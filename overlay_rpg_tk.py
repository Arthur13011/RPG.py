import codecs
import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class RPGOverlay:
    def __init__(self, master, rpg_path):
        self.master = master
        self.rpg_path = os.path.abspath(rpg_path)
        self.proc = None
        self.output_queue = queue.Queue()

        master.title("RPG.py")
        master.geometry("900x600")
        master.configure(bg="black")

        try:
            master.attributes("-topmost", True)
        except tk.TclError:
            pass

        self.text = ScrolledText(
            master,
            wrap="word",
            state="disabled",
            bg="black",
            fg="white",
            font=("Consolas", 12),
        )
        self.text.pack(fill="both", expand=True)

        entry_frame = tk.Frame(master, bg="black")
        entry_frame.pack(fill="x")

        self.entry = tk.Entry(
            entry_frame,
            font=("Consolas", 12),
            bg="#111",
            fg="white",
            insertbackground="white",
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(4, 2), pady=4)
        self.entry.bind("<Return>", self.send_input)

        send_btn = tk.Button(
            entry_frame,
            text="Send",
            command=self.send_input,
            bg="#222",
            fg="white",
        )
        send_btn.pack(side="right", padx=(2, 4), pady=4)

        master.protocol("WM_DELETE_WINDOW", self.on_close)
        master.after(30, self._flush_output)
        self._start_process()

    def _start_process(self):
        if not os.path.isfile(self.rpg_path):
            self.output_queue.put(
                f"Could not find RPG.py at:\n{self.rpg_path}\n"
            )
            return

        cwd = os.path.dirname(self.rpg_path)
        cmd = [sys.executable, "-u", "-X", "utf8", os.path.basename(self.rpg_path)]
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"

        try:
            self.proc = subprocess.Popen(
                cmd,
                cwd=cwd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,
            )
        except Exception as exc:
            self.output_queue.put(f"Could not start RPG.py:\n{exc}\n")
            return

        threading.Thread(target=self._reader_thread, daemon=True).start()

    def _reader_thread(self):
        if self.proc is None or self.proc.stdout is None:
            return

        decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        try:
            while True:
                raw = os.read(self.proc.stdout.fileno(), 4096)
                if not raw:
                    break

                chunk = decoder.decode(raw)
                if chunk:
                    self.output_queue.put(chunk)

            remaining = decoder.decode(b"", final=True)
            if remaining:
                self.output_queue.put(remaining)

        except Exception as exc:
            self.output_queue.put(f"\n[Output reader error: {exc}]\n")
        finally:
            code = self.proc.poll() if self.proc is not None else None
            self.output_queue.put(f"\n[Process exited with code {code}]\n")

    def _flush_output(self):
        pieces = []
        while True:
            try:
                pieces.append(self.output_queue.get_nowait())
            except queue.Empty:
                break

        if pieces:
            try:
                self.text.configure(state="normal")
                self.text.insert("end", "".join(pieces))
                self.text.see("end")
                self.text.configure(state="disabled")
            except tk.TclError:
                return

        if self.master.winfo_exists():
            self.master.after(30, self._flush_output)

    def send_input(self, event=None):
        if self.proc is None or self.proc.poll() is not None:
            self.output_queue.put("\n[The RPG process is not running.]\n")
            return "break"

        if self.proc.stdin is None:
            self.output_queue.put("\n[Input pipe is unavailable.]\n")
            return "break"

        text = self.entry.get()
        try:
            self.proc.stdin.write((text + "\n").encode("utf-8"))
            self.proc.stdin.flush()
            self.entry.delete(0, "end")
        except (BrokenPipeError, OSError, ValueError) as exc:
            self.output_queue.put(f"\n[Could not send input: {exc}]\n")

        return "break"

    def on_close(self):
        try:
            if self.proc is not None and self.proc.poll() is None:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
        except Exception:
            pass

        try:
            self.master.destroy()
        except tk.TclError:
            pass


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(folder, "RPG.py")

    if not os.path.isfile(script_path):
        print(f"Could not find RPG.py at: {script_path}")
        print("Put RPG.py in the same folder as this overlay, or update script_path.")
        return

    root = tk.Tk()
    RPGOverlay(root, script_path)
    root.mainloop()


if __name__ == "__main__":
    main()

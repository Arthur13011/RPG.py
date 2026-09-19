import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import codecs
import subprocess
import threading
import sys
import os


class RPGOverlay:
    def __init__(self, master, rpg_path):
        self.master = master
        self.rpg_path = rpg_path
        master.title('RPG.py ')
        master.geometry('900x600')
        master.configure(bg='black')
        # keep the overlay on top of other windows
        try:
            master.attributes('-topmost', True)
        except Exception:
            pass

        self.text = ScrolledText(master, wrap='word', state='disabled', bg='black', fg='white', font=('Consolas', 12))
        self.text.pack(fill='both', expand=True)

        entry_frame = tk.Frame(master, bg='black')
        entry_frame.pack(fill='x')
        self.entry = tk.Entry(entry_frame, font=('Consolas', 12), bg='#111', fg='white', insertbackground='white')
        self.entry.pack(side='left', fill='x', expand=True, padx=(4, 2), pady=4)
        self.entry.bind('<Return>', self.send_input)
        send_btn = tk.Button(entry_frame, text='Send', command=self.send_input, bg='#222', fg='white')
        send_btn.pack(side='right', padx=(2, 4), pady=4)

        self.proc = None
        self._start_process()

        master.protocol('WM_DELETE_WINDOW', self.on_close)

    def _start_process(self):
        # Launch RPG.py as a subprocess and capture stdout/stderr
        cwd = os.path.dirname(self.rpg_path)
        # run the game unbuffered with UTF-8 to avoid garbled/late output
        cmd = [sys.executable, '-u', '-X', 'utf8', os.path.basename(self.rpg_path)]
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        self.proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
        self.proc_stdout = codecs.getreader('utf-8')(self.proc.stdout, errors='replace')

        # Thread to read stdout
        threading.Thread(target=self._reader_thread, daemon=True).start()

    def _reader_thread(self):
        try:
            while True:
                chunk = self.proc_stdout.read(1)
                if chunk == '':
                    break
                self._append_text(chunk)
        except Exception:
            pass
        finally:
            exit_code = self.proc.poll()
            self._append_text(f"\n[Process exited with code {exit_code}]\n")

    def _append_text(self, s):
        def _do():
            self.text.configure(state='normal')
            self.text.insert('end', s)
            self.text.see('end')
            self.text.configure(state='disabled')
        self.text.after(0, _do)

    def send_input(self, event=None):
        if not self.proc or self.proc.poll() is not None:
            return
        text = self.entry.get()
        try:
            # write and flush to subprocess stdin in UTF-8
            self.proc.stdin.write((text + '\n').encode('utf-8'))
            self.proc.stdin.flush()
        except Exception:
            pass
        self.entry.delete(0, 'end')

    def on_close(self):
        try:
            if self.proc and self.proc.poll() is None:
                self.proc.terminate()
        except Exception:
            pass
        self.master.destroy()


def main():
    script_path = os.path.join(os.path.dirname(__file__), 'RPG.py')
    if not os.path.exists(script_path):
        print('Could not find RPG.py at', script_path)
        return
    root = tk.Tk()
    app = RPGOverlay(root, script_path)
    root.mainloop()


if __name__ == '__main__':
    main()
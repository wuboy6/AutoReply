import subprocess
import time


class Ollama:
    llamas = {
        "ms": "phi3:14b",
        "llama":"llama3.2:3b",
        "vision": "llama3.2-vision:11b",
        "coder": "qwen2.5-coder:14b"
    }
    ollama_process = subprocess.Popen(
        ['/bin/zsh'],  # 或者 '/bin/bash'
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    is_ollama_init = False

    def __init__(self,llama_name):
        if(llama_name in self.llamas):
            self.llama = self.llamas[llama_name]
        else:
            self.llama = self.llama["llama"]

        #初始化ollama
        if(self.is_ollama_init == False):
            self.is_ollama_init = True
            self.ollama_process.stdin.write('ollama serve\n')
            self.ollama_process.stdin.flush()
            print("Ollama已完成初始化")

        #runAI模型
        self.llama_process = subprocess.Popen(
            ['/bin/zsh'],  # 或者 '/bin/bash'
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=4096
        )
        self.llama_process.stdin.write("ollama run "+self.llama+"\n")
        self.llama_process.stdin.flush()

    def line_reply(self,text):
        #TODO： 实现连续的回复，正在开发
        self.llama_process.stdin.write(text + "\n")
        self.llama_process.stdin.flush()
        print("Waiting for reply")

        self.llama_process.stdout.flush()

        output = ""
        size = 0
        while(len(output) ==0 or len(output) > size):
            self.llama_process.stdout.flush()
            print(2)
            output += self.llama_process.stdout.read()


        print(output)
        reply = 1
        return reply

    def sperate_reply(self,text):
        process = subprocess.Popen(
            ['/bin/zsh'],  # 或者 '/bin/bash'
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=4096
        )
        process.stdin.write("ollama run " + self.llama + "\n")
        process.stdin.flush()

        print("正在生成sperate回复，请稍等")

        process.stdin.write(text + "\n")
        process.stdin.flush()

        output, error = process.communicate()
        return output

    def renew(self):
        self.llama_process = subprocess.Popen(
            ['/bin/zsh'],  # 或者 '/bin/bash'
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=-1
        )
        self.llama_process.stdin.write("ollama run " + self.llama + "\n")
        self.llama_process.stdin.flush()
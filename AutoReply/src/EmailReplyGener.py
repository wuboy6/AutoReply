from Ollama import Ollama

email_llama = Ollama("vision")

def email_bind_llama(self, ollama):
    email_llama = ollama
# 示例：用于生成回复内容的类
class AutoEmailReplyGenerator:

    @staticmethod
    def generate_reply(sender, content):
        print(content)
        text = "我收到了一封邮件，请帮我直接生成回复内容，你的回复第一行写邮件主题，从第二行开始写正文。邮件的发送者是"+str(sender)+",邮件内容是"+str(content)
        response = email_llama.sperate_reply(content )

        subject = f"{sender},我已收到您的邮件"
        body = response

        print(f"已为{sender}生成回复信:{response}")

        return subject, body
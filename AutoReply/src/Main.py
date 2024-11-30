from Ollama import Ollama
import time
import EmailReplyGener
from EmailReplyGener import AutoEmailReplyGenerator

#ol = Ollama("llama")

# reply = ol.sperate_reply("你好")
# print(reply)

from Email import Email

if __name__ == "__main__":
    # 配置邮箱信息
    email = Email(
        imap_server="imap.88.com",  # 88 的 IMAP 服务器地址
        smtp_server="smtp.88.com",  # 88 的 SMTP 服务器地址
        email_address="autococo@88.com",  # 你的 88 邮箱地址
        email_password=""  # 你的邮箱密码
    )

    while(True):
        email.run(AutoEmailReplyGenerator.generate_reply)
        time.sleep(10)

import imaplib
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr
from email import message_from_bytes


class Email:
    def __init__(self, imap_server, smtp_server, email_address, email_password):
        """
        初始化Email类

        :param imap_server: IMAP服务器地址
        :param smtp_server: SMTP服务器地址
        :param email_address: 邮箱地址
        :param email_password: 邮箱密码
        """
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email_address = email_address
        self.email_password = email_password
        self.mail = None

    def connect_to_imap(self):
        """连接到IMAP服务器"""
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_address, self.email_password)
        self.mail.select("inbox")

    def get_unread_emails(self):
        """
        获取未读邮件的发件人和正文内容

        :return: 包含未读邮件信息的列表，每个元素为一个字典，包含"from"和"body"
        """
        status, messages = self.mail.search(None, 'UNSEEN')
        if status != 'OK':
            return []

        unread_emails = []
        for num in messages[0].split():
            status, data = self.mail.fetch(num, '(RFC822)')
            if status != 'OK':
                continue

            _, msg_data = data[0]
            msg = message_from_bytes(msg_data)  # 使用email库解析邮件

            email_info = {"from": None, "body": None}

            # 获取发件人
            for header in msg.keys():
                if header.lower() == "from":
                    email_info["from"] = parseaddr(msg.get(header))[1]
                    break

            # 提取正文内容
            body = self.extract_body(msg)
            email_info["body"] = body

            unread_emails.append(email_info)
        return unread_emails

    def extract_body(self, msg):
        """
        提取邮件正文，支持纯文本和HTML格式

        :param msg: 邮件消息对象
        :return: 邮件正文内容
        """
        body = None
        if msg.is_multipart():  # 如果是多部分邮件
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # 只提取文本内容
                if "attachment" not in content_disposition:
                    if content_type == "text/plain":  # 提取纯文本正文
                        body = part.get_payload(decode=True).decode()
                        break
                    elif content_type == "text/html":  # 提取HTML正文
                        body = part.get_payload(decode=True).decode()
        else:  # 如果是单一邮件（非多部分）
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                body = msg.get_payload(decode=True).decode()
            elif content_type == "text/html":
                body = msg.get_payload(decode=True).decode()

        return body

    def send_email(self, to_address, subject, body):
        """
        发送邮件

        :param to_address: 收件人地址
        :param subject: 邮件主题
        :param body: 邮件正文
        """
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = self.email_address
        msg["To"] = to_address
        msg["Subject"] = subject

        with smtplib.SMTP_SSL(self.smtp_server) as server:
            server.login(self.email_address, self.email_password)
            server.sendmail(self.email_address, to_address, msg.as_string())

    def run(self, reply_generator):
        """
        运行自动回复流程

        :param reply_generator: 一个函数，接受发件人和内容参数，并返回回复内容
        """
        try:
            self.connect_to_imap()
            unread_emails = self.get_unread_emails()
            for email_info in unread_emails:
                sender = email_info["from"]
                content = email_info["body"]
                reply_subject, reply_body = reply_generator(sender, content)
                self.send_email(sender, reply_subject, reply_body)
            self.mail.logout()
        except Exception as e:
            print(f"运行时发生错误: {e}")


# 示例：用于生成回复内容的类
class AutoReplyGenerator:
    @staticmethod
    def generate_reply(sender, content):
        """
        根据发件人和内容生成自动回复

        :param sender: 发件人地址
        :param content: 邮件内容
        :return: 回复的主题和正文
        """
        subject = "自动回复: 我已收到您的邮件"
        body = f"""
您好，{sender}：

感谢您的来信！我目前无法立即回复您的邮件，但我会尽快回复您。

祝好！
"""
        return subject, body
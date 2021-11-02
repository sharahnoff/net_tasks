import os
import mimetypes
import time
import base64

BOUNDARY = ""

def get_file_content(filename):
    with open(filename, "rb") as f:
        image_str = f.read()
        return base64.b64encode(image_str).decode()

def get_text(filename):
    with open(filename, "r", encoding="utf8") as f:
        message = "".join(f.readlines())
        content = ""
        content += f"Content-Transfer-Encoding: 8bit\n"
        content += f"Content-Type: text/plain; charset=utf-8\n\n"
        content += message.replace("\n.", "\n..")
        return content

def get_base64string(msg):
    return base64.b64encode(msg.encode()).decode()

def get_header(user, user_adr, targets, subject):
    targets_addr = ",".join(f"\"{x}\" <{x}>" for x in targets)
    header = ""
    header += f"From: \"{user}\" <{user_adr}>\n"
    header += f"To:{targets_addr}\n"
    header += f"Subject: =?UTF-8?B?{get_base64string(subject)}?=\n"
    header += f"Content-type: multipart/mixed; boundary={BOUNDARY}\n\n"
    return header

def append(m1, m2):
    m1 += f"--{BOUNDARY}" + "\n" + m2
    return m1

def create_attachment(filename):
    filename = f"./configs/attachments/{filename}"
    fname, extension = os.path.splitext(filename)
    mimetypes.init()
    mime = mimetypes.types_map[extension]
    name = filename.split("/")[-1]
    base64_filename = f"=?UTF-8?B?{get_base64string(name)}?="
    base64_attachment = get_file_content(filename)
    content = f"Content-Type: {mime}; name=\"{base64_filename}\"\n"
    content += f"Content-Disposition: attachment; filename=\"{base64_filename}\"\n"
    content += f"Content-Transfer-Encoding: base64\n\n"
    content += base64_attachment
    return content

def create_message(message_file, user, user_adr, targets, subject, attachment):
    subject = subject or "No subject"
    message = get_header(user, user_adr, targets, subject)
    message = append(message, get_text(message_file))
    if not attachment:
        return message + str(f"\n--{BOUNDARY}--\n.\n")
    attachments = [create_attachment(x) for x in attachment]
    for att in attachments:
        message = append(message, att)
    return message + str(f"\n--{BOUNDARY}--\n.\n")


if __name__ != "__main__":
    BOUNDARY = "kdsljflsdkjf" + str(time.time()) + "lkdsjflsdkjfldskj"
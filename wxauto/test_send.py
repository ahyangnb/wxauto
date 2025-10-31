from wxauto import WeChat

# Initialize WeChat instance (make sure WeChat is running and logged in)
wx = WeChat()

# Send a message
# wx.SendMsg("你好", who="文件传输助手")  # Send to File Transfer
wx.SendMsg("你11好", who="ahyang")  # Send to File Transfer

# Get messages from current chat window
msgs = wx.GetAllMessage()
for msg in msgs:
    print(f"{msg.sender}: {msg.content}")
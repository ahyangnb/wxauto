"""
Listener that handles build commands from WeChat messages.
If user sends "帮助", responds with available commands.
If user sends a command (1-5), responds with processing status.
Make sure WeChat desktop is running and you're logged in before running this script.
"""

from wxauto import WeChat
from wxauto.msgs import FriendMessage

# Task descriptions mapping
TASKS = {
    "1": "打包测试环境官网包",
    "2": "打包测试环境商店包",
    "3": "打包正式官网包",
    "4": "打包正式环境商店包",
    "5": "打包aab"
}

def on_message(msg, chat):
    """Callback function that handles incoming messages"""
    # Only respond to text messages from friends (not your own messages)
    if isinstance(msg, FriendMessage) and msg.type == 'text':
        # Get the original message content
        original_msg = msg.content.strip()
        
        print(f"Received: {original_msg}")
        
        # Handle "帮助" command
        if original_msg == "帮助":
            help_msg = "1=打包测试环境官网包；2.打包测试环境商店包；3. 打包正式官网包；4. 打包正式环境商店包；5. 打包aab。"
            print(f"Sending: {help_msg}")
            chat.SendMsg(help_msg)
            return
        
        # Handle command numbers (1-5)
        if original_msg in TASKS:
            task_desc = TASKS[original_msg]
            reply_msg = f"开始处理：{task_desc}"
            print(f"Sending: {reply_msg}")
            chat.SendMsg(reply_msg)
            return

def main():
    print("Initializing WeChat instance...")
    wx = WeChat()
    
    # Only listen to messages from "ahyang"
    nickname = "ahyang"
    
    print(f"Adding listener for: {nickname}")
    
    # Add the listener
    result = wx.AddListenChat(nickname=nickname, callback=on_message)
    
    if hasattr(result, '_api'):  # Success - returns Chat object
        print(f"✅ Successfully listening to {nickname}")
        print("Listening for messages... (Press Ctrl+C to stop)")
    else:
        print(f"❌ Failed to add listener: {result}")
        return
    
    # Keep the program running
    try:
        wx.KeepRunning()
    except KeyboardInterrupt:
        print("\nStopping listener...")
        wx.StopListening()
        print("Listener stopped.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure:")
        print("1. WeChat desktop client is running")
        print("2. You are logged into WeChat")
        print("3. The contact name is correct")


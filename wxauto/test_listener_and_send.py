"""
Listener that receives messages and sends back the same message + "+1"
Make sure WeChat desktop is running and you're logged in before running this script.
"""

from wxauto import WeChat
from wxauto.msgs import FriendMessage

def on_message(msg, chat):
    """Callback function that handles incoming messages"""
    # Only respond to text messages from friends (not your own messages)
    if isinstance(msg, FriendMessage) and msg.type == 'text':
        # Get the original message content
        original_msg = msg.content
        
        # Send back the same message + "+1"
        reply_msg = original_msg + "+1"
        
        print(f"Received: {original_msg}")
        print(f"Sending: {reply_msg}")
        
        # Send the reply
        chat.SendMsg(reply_msg)

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


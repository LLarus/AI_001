import os
from dashscope import Generation

# 存储对话历史
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}
]


def get_response(user_input):
    # 向消息列表添加用户输入
    messages.append({'role': 'user', 'content': user_input})

    # 调用 DashScope API 获取响应
    try:
        responses = Generation.call(
            api_key=os.getenv('DASHSCOPE_API_KEY'),  # 从环境变量获取 API Key
            model="qwen-plus",
            messages=messages,
            result_format="message",
            stream=True,
            incremental_output=True
        )

        assistant_reply = ""
        print("助手：", end='', flush=True)

        # 流式处理响应
        for response in responses:
            chunk_content = response.output.choices[0].message.content
            assistant_reply += chunk_content
            print(chunk_content, end='', flush=True)

        print()  # 输出换行
        # 更新对话历史
        messages.append({'role': 'assistant', 'content': assistant_reply})
        return assistant_reply

    except Exception as e:
        print("\n[错误] 无法获取响应，请检查网络或 API Key。")
        return "抱歉，我暂时无法处理您的请求。"


# 主程序：处理用户输入
def main():
    print("欢迎使用 AI 助手！输入'再见'即可退出。")
    while True:
        user_input = input("用户: ").strip()
        if not user_input:
            print("输入为空，请重新输入。")
            continue

        # 检查是否结束对话
        if any(kw in user_input for kw in ["再见", "就这样吧", "拜拜"]):
            print("助手：感谢您的咨询，再见！")
            break

        # 获取回复
        get_response(user_input)


if __name__ == "__main__":
    main()

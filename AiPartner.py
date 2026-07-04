import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import random
import json

API_KEY = os.environ.get("OPENAI_API_KEY", "")
st.set_page_config(
    page_title = "赛博周易",
    page_icon = "🤖",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {}
)

# 保存当前会话的方法
def save_current_session():
    if st.session_state.current_session:
        # 构建会话对象
        session_date = {
            # "nick_name": st.session_state.nick_name,
            # "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
            "gua": st.session_state.gua
        }
        # 如果不存在创建文件夹
    if not os.path.exists("session"):
        os.mkdir("session")
        # 保存会话数据
    with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
        json.dump(session_date, f, ensure_ascii=False, indent=4)

# 生成会话标识
def generate_current_session():
    return datetime.now().strftime("%Y-%m-%d %H_%M_%S")

# 生成空的会话数据
def generate_session_messages():
    return []

gua_list = ["乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复", "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济"]
# 从64卦中随机生成一个
def random_gua():
    return random.choice(gua_list)

# 加载所有的会话列表信息
def load_sessions():
    session_list = []
    # 加载session目录下的文件
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for file_name in file_list:
            if file_name.endswith(".json"):
                session_list.append(file_name[:-5])
        session_list.sort(reverse=True)  # 对返回的结果进行排序 倒叙
        return session_list

# 加载指定对话
def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            # 读取会话数据
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:
                session_date = json.load(f)
                st.session_state.messages = session_date["messages"]
                # st.session_state.nick_name = session_date["nick_name"]
                # st.session_state.nature = session_date["nature"]
                st.session_state.current_session = session_name
                st.session_state.gua = session_date["gua"]
    except Exception as e:
        print(f"加载会话出错：{e}")
        st.error("加载会话失败！")

# 删除会话
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
           # 如果存在删除对话
            os.remove(f"session/{session_name}.json")
            # 如果删除的是当前会话需要清空消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = generate_session_messages()
                st.session_state.current_session = generate_current_session()
    except Exception as e:
        print(f"删除会话出错：{e}")
        st.error("删除会话失败！")


# 大标题
st.title("赛博大师")

# logo
st.logo("resource/logo.png")

# 系统提示此
sys_prompt = """
    你叫林晚，现在是26岁精通周易六十四卦、五行、易学的大师，请完全代入该角色角色。：
    规则：
        1、每次只回复一条消息
        2、禁止任何场景或状态描述性文字
        3、匹配用户的语言
        4、结合用户的问题和对卦的解读，明确的回复用户
        5、用符合易学大师性格的方式对话
        6、回复的内容要充分的体现易学大师的性格特征
    易学大师性格：
        - 精通周易八卦 能够详细解读已经六十四卦
    本次卦名为 %s
    你必须严格遵守上述规则回复用户
"""


# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = generate_session_messages()
# 昵称
# if "nick_name" not in st.session_state:
#     st.session_state.nick_name = "林晚"
# 性格
# if "nature" not in st.session_state:
#     st.session_state.nature = "有活力温柔细心活泼的河北姑娘"
# 会话名称
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_current_session()

# 摇到的卦：
if "gua" not in st.session_state:
    st.session_state.gua = ""

# 展示当前会话名称
st.text(f"会话名称：{st.session_state.current_session}")

# 展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 创建与ai大模型交互的客户端
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# 定义左侧侧边栏  with是streamlit中的上下文管理器
with st.sidebar:
    # 控制面板
    st.subheader("控制面板")
    # 新建会话的按钮
    if st.button("新建会话", width="stretch", icon="🔄"):
        # 保存当前会话数据
        save_current_session()
        # 创建新的会话
        # 生成新的会话名称
        if st.session_state.messages:
            st.session_state.current_session = generate_current_session()
            # 生成新的会话列表
            st.session_state.messages = generate_session_messages()
            save_current_session()
            st.rerun() #streamlit的加载机制-先重新加载页面再执行点击按钮的方法  所以需要手动调用重新加载页面

    # 会话历史
    st.text("历史会话")
    session_list = load_sessions()
    if session_list:
        for session in session_list:
            col1,col2 = st.columns([4,1])
            with col1:
                # 加载指定对话
                if st.button(session, width="stretch", icon="🗂",key=f"load_{session}", type="primary" if session == st.session_state.current_session else "secondary"):
                    load_session(session)
                    st.rerun()
            with col2:
                # 删除指定对话
                if st.button("", width="stretch", icon="❌",key=f"delete_{session}"):
                    delete_session(session)
                    st.rerun()

    # 分割线
    st.divider()

    if st.button("摇一摇", width="stretch", icon="🎲"):
        st.session_state.gua = random_gua()

    # 将摇到的卦展示出来
    st.text(f"摇到的卦：{st.session_state.gua}")
    #
    # # 侧边栏标题
    # st.subheader("伙伴信息")
    # # 伙伴名称
    # nick_name = st.text_input("伙伴名称",placeholder="请输入伙伴名称",value=st.session_state.nick_name)
    # if nick_name:
    #     st.session_state.nick_name = nick_name
    # # 性格输入框
    # nature = st.text_area("伙伴性格",placeholder="请输入伙伴性格",value=st.session_state.nature)
    # if nature:
    #     st.session_state.nature = nature

# 消息输入
prompt =  st.chat_input("聊些什么~")
if prompt:
    st.chat_message("user").write(prompt)
    print(f"调用ai大模型，输入的提示词：{prompt}")
    # 保存用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用ai大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": sys_prompt % st.session_state.gua},
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "disabled"}}
    )
    # 输出大模型返回的结果
    # 非流式输出解析方式  response.choices[0].message.content
    # print(f"<--------大模型返回的结果：{response.choices[0].message.content}")
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # 流式输出解析方式
    response_message = st.empty()  #创建一个空容器用于展示大模型返回的结果
    result = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            result += content
            response_message.chat_message("assistant").write(result)
    print(f"<--------大模型返回的结果：{result}")
    #保存大模型返回内容
    st.session_state.messages.append({"role": "assistant", "content": result})
    # 保存会话信息
    save_current_session()
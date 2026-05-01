# WClaw 个人 Agent 骨架

`WClaw` 是一个基于 `DeepAgent` 搭建的个人 Agent 项目骨架。


## 目录结构

```text
.
├─ __main__.py
├─ README.md
├─ requirements.txt
├─ agent/
│  ├─ __init__.py
│  └─ main_agent.py
├─ config/
│  └─ config.yaml
├─ runtime/
│  ├─ __init__.py
│  ├─ formatting.py
│  └─ runner.py
├─ subagents/
│  ├─ __init__.py
│  └─ factory.py
├─ tools/
│  └─ __init__.py
├─ utils/
│  ├─ __init__.py
│  ├─ config_loader.py
│  └─ env_utils.py
└─ skills/
```

## 运行方式

```bash
pip install -r requirements.txt
python __main__.py
```

## 模块职责

- `__main__.py`：项目启动入口
- `agent/main_agent.py`：创建主智能体
- `subagents/factory.py`：根据配置装配子智能体
- `config/config.yaml`：保存静态配置
- `utils/config_loader.py`：读取并解析配置
- `utils/env_utils.py`：设置运行时环境变量
- `runtime/runner.py`：执行默认演示任务
- `runtime/formatting.py`：格式化智能体输出

## 后续建议

比较适合继续补充的能力有：

1. 会话记忆
2. 能力注册机制
3. 失败重试与回退
4. 真实的小红书发布 skill

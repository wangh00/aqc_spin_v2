# 百度旋转验证码逆向（aqc_spin_v2）

复刻百度 wappass 旋转验证码（spin）的完整校验流程，纯协议实现，**校验通过返回 `op=1`**。

> 分析过程：[CSDN 文章](https://blog.csdn.net/wh00011/article/details/140658471)
> 识别模型：[rotate_image_classifier](https://github.com/HarderThenHarder/rotate_image_classifier)

## 流程概览

```
POST /cap/init    -> 拿 tk / as / ds / ls
POST /cap/style   -> 拿 backstr、captchalist(spin-0)、ext.p(pow 参数)
GET  /cap/img     -> 下载旋转验证码原图（350x350 JPEG）
模型识别          -> 预测需要旋转的角度
生成轨迹          -> mv1(拖动) / mv2(旋转) / ac_c
AES-ECB 加密      -> fs1、fs2（key 由 as 推导）
POST /cap/log     -> op=1 表示校验通过
```

## 运行环境

- Python **3.10 / 3.11**（3.12 也可，需自行安装 torch 等依赖）
- **Node.js**（`sha3.js` 依赖 `crypto-js`，仓库已带 `node_modules`）
- 依赖见 `requirements.txt`，关键包：
  - `requests`、`opencv-python`、`numpy`、`pillow`
  - `torch`、`torchvision`
  - `pycryptodome`（AES）
  - `PyExecJS`（执行 `sha3.js` 计算 pow）

安装：

```bash
pip install -r requirements.txt
```

## 使用

```bash
python aqc_spin_v2.py
```

如果默认 `python` 没装 torch，请指定装了依赖的解释器，例如：

```powershell
D:\miniconda\envs\test_py311\python.exe aqc_spin_v2.py
```

运行成功时输出：

```
旋转验证码校验成功!获得返回结果: 1
```

单次识别失败（返回 `op=3`）时代码会自动刷新验证码并重试，直到拿到 `op=1`。

## 目录结构

| 文件 | 说明 |
|---|---|
| `aqc_spin_v2.py` | 主流程：请求、轨迹、AES 加密、提交校验 |
| `init_style.py` | `/cap/init`、`/cap/style` 接口封装 |
| `rotate_image_classifier_inference.py` | 角度识别推理 |
| `utils.py` | 数据集与图像预处理 |
| `sha3.js` | pow 计算（Node + crypto-js） |
| `models/model_13.pth` | 角度识别模型权重 |
| `img_file/` | 验证码图片输出目录 |

## 接口与参数（2026-11 实测）

| 接口 | 关键返回 |
|---|---|
| `POST /cap/init` | `tk`、`as`、`ds`、`ls` |
| `POST /cap/style` | `backstr`、`captchalist[0].id=spin-0`、`ext.p`（pow 参数） |
| `GET passport.baidu.com/cap/img` | 旋转验证码图片 |
| `POST /cap/log` | `data.op`：**1 = 成功**，**3 = 角度答错** |

关于 `op=3`：早期版本认为是"未携带校验参数"，实测结论是**角度判断错误**——
同一套请求流程，按模型预测角度提交返回 `op=1`，故意偏移 180° 提交则必返回 `op=3`。

## 已知问题

- **识别准确率**：模型单次预测准确率约 40%~50%，靠失败自动换图重试最终成功；重试为递归且无上限，长时间失败会持续发请求，可按需加上限。
- **torch 版本**：`torch>=2.6` 的 `torch.load` 默认 `weights_only=True`，本项目已显式传 `weights_only=False`；老版本 torch 同样兼容。
- **`wget` 依赖**：仅训练集下载（`utils.download()`）需要，已改为惰性导入，推理环境无需安装。
- **网络/代理**：若出现 `SSLEOFError`（TLS 握手被中断），通常是本地代理 fake-ip 路由问题，与本项目无关；重启代理或改用真实 IP 即可。
- **Cookie**：代码中的 `BAIDUID` / `RT` 为示例值，长期使用建议替换成自己的。

## 更新记录

- **2026-11**
  - 兼容 `torch>=2.6`（`torch.load(..., weights_only=False)`）
  - `wget` 改为惰性导入，推理环境不再强依赖
  - 实测并更正 `op=3` 含义：角度错误，而非参数缺失
  - README 重写，补充依赖与已知问题
- **2024-08-05**
  - 新增校验参数（`fuid` 等），未携带会返回 `op=3`（当时的结论）
- 历史运行截图：[pkvXAiV.png](https://s21.ax1x.com/2024/08/05/pkvXAiV.png)

## 声明

本项目仅用于学习与技术研究，请勿用于任何商业或非法用途；接口与风控随时可能变化，不保证长期可用。

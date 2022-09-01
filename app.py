import numpy as np
import gradio as gr
import paddlehub as hub


model = hub.Module(name='ernie_vilg')
style_list = ['水彩','油画', '粉笔画', '卡通', '蜡笔画', '儿童画', '探索无限']
def inference(text_prompts, style_indx):
  try:
    style = style_list[style_indx]
    results = model.generate_image(
        text_prompts=text_prompts, style=style, visualization=False)
    return 'Success', results[:6]
  except Exception as e:
    error_text = str(e)
    return error_text, None
  return


title="ERNIE-ViLG"

description="ERNIE-ViLG model, which supports text-to-image task."

css = """
        .gradio-container {
            font-family: 'IBM Plex Sans', sans-serif;
        }
        .gr-button {
            color: white;
            border-color: black;
            background: black;
        }
        input[type='range'] {
            accent-color: black;
        }
        .dark input[type='range'] {
            accent-color: #dfdfdf;
        }
        .container {
            max-width: 730px;
            margin: auto;
            padding-top: 1.5rem;
        }
        #gallery {
            min-height: 22rem;
            margin-bottom: 15px;
            margin-left: auto;
            margin-right: auto;
            border-bottom-right-radius: .5rem !important;
            border-bottom-left-radius: .5rem !important;
        }
        #gallery>div>.h-full {
            min-height: 20rem;
        }
        .details:hover {
            text-decoration: underline;
        }
        .gr-button {
            white-space: nowrap;
        }
        .gr-button:focus {
            border-color: rgb(147 197 253 / var(--tw-border-opacity));
            outline: none;
            box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
            --tw-border-opacity: 1;
            --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
            --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(3px var(--tw-ring-offset-width)) var(--tw-ring-color);
            --tw-ring-color: rgb(191 219 254 / var(--tw-ring-opacity));
            --tw-ring-opacity: .5;
        }
        .footer {
            margin-bottom: 45px;
            margin-top: 35px;
            text-align: center;
            border-bottom: 1px solid #e5e5e5;
        }
        .footer>p {
            font-size: .8rem;
            display: inline-block;
            padding: 0 10px;
            transform: translateY(10px);
            background: white;
        }
        .dark .footer {
            border-color: #303030;
        }
        .dark .footer>p {
            background: #0b0f19;
        }
        .prompt h4{
            margin: 1.25em 0 .25em 0;
            font-weight: bold;
            font-size: 115%;
        }
"""

block = gr.Blocks(css=css)

examples = [
    [
        '戴着眼镜的猫',
        '油画(Oil painting)'
    ],
    [
        '日落时的城市天际线,史前遗迹风格',
        '油画(Oil painting)'
    ],
    [
        '一只猫坐在椅子上，戴着一副墨镜, low poly 风格',
        '卡通(Cartoon)'
    ],
    [
        '一只猫坐在椅子上，戴着一副墨镜,秋天风格',
        '探索无限(Explore infinity)'
    ],
    [
        '蒙娜丽莎，赛博朋克，宝丽来，33毫米,蒸汽波艺术',
        '探索无限(Explore infinity)'
    ],
    [
        '一只猫坐在椅子上，戴着一副墨镜,海盗风格',
        '探索无限(Explore infinity)'
    ],
    [
        '一条由闪电制成的令人敬畏的龙,概念艺术',
        '探索无限(Explore infinity)'
    ],
    [
        '梵高猫头鹰,蒸汽波艺术',
        '探索无限(Explore infinity)'
    ],
    [
        '萨尔瓦多·达利描绘古代文明的超现实主义梦幻油画,写实风格',
        '探索无限(Explore infinity)'
    ],
    [
        '夕阳日落时，阳光落在云层上，海面波涛汹涌，风景，胶片感',
        '探索无限(Explore infinity)'
    ]
]

with block:
    gr.HTML(
        """
            <div style="text-align: center; max-width: 650px; margin: 0 auto;">
              <div
                style="
                  display: inline-flex;
                  align-items: center;
                  gap: 0.8rem;
                  font-size: 1.75rem;
                  margin-bottom: 10px;
                  justify-content: center;
                "
              >
              <img src="https://user-images.githubusercontent.com/22424850/187387422-f6c9ccab-7fda-416e-a24d-7d6084c46f67.jpg" alt="Paddlehub" width="40%">
              </div> 
              <div
                style="
                  display: inline-flex;
                  align-items: center;
                  gap: 0.8rem;
                  font-size: 1.75rem;
                  margin-bottom: 10px;
                  justify-content: center;
                ">
              <h1 style="font-weight: 900; margin-bottom: 7px;">
                  ERNIE-ViLG Demo
              </h1>
              </div> 
              <p style="margin-bottom: 10px; font-size: 94%">
                ERNIE-ViLG is a state-of-the-art text-to-image model that generates
                images from Chinese text.
              </p>
            </div>
        """
    )
    with gr.Group():
        with gr.Box():
            with gr.Row().style(mobile_collapse=False, equal_height=True):
                text = gr.Textbox(
                    label="Prompt (Chinese)",
                    show_label=False,
                    max_lines=1,
                    placeholder="Enter your Chinese prompt",
                ).style(
                    border=(True, False, True, True),
                    rounded=(True, False, False, True),
                    container=False,
                )
                btn = gr.Button("Generate image").style(
                    margin=False,
                    rounded=(False, True, True, False),
                )
        styles = gr.Dropdown(label="style（风格）", choices=['水彩(Watercolor)','油画(Oil painting)', '粉笔画(Chalk drawing)', '卡通(Cartoon)', '蜡笔画(Crayon drawing)', '儿童画(Children\'s drawing)', '探索无限(Explore infinity)'], value='探索无限(Explore infinity)', type="index")
        gallery = gr.Gallery(
            label="Generated images", show_label=False, elem_id="gallery"
        ).style(grid=[2, 3], height="auto")
        status_text = gr.Textbox(
            label="Process status（处理状态）",
            show_label=True,
            max_lines=1,
            interactive=False
        )
        
        ex = gr.Examples(examples=examples, fn=inference, inputs=[text, styles], outputs=gallery, cache_examples=False)
        ex.dataset.headers = [""]

        
        text.submit(inference, inputs=[text, styles], outputs=[status_text, gallery])
        btn.click(inference, inputs=[text, styles], outputs=[status_text, gallery])
        gr.HTML(
            """
                <div class="prompt">
                    <p><h4>Prompt公式</h4>
                    <span> Prompt = [形容词] [主语] ，[细节设定]， [修饰语或者艺术家]。 </span>
                    关于各部分的构造方式和效果，可以参考<a href="https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#四-prompt-指南" style="text-decoration: underline;" target="_blank">YouPromptMe指南</a>。
                    更多的模型，请关注<a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank"> PaddleHub 官方Repo </a>， 并star收藏。
                    同时，可以在 <a href="https://aistudio.baidu.com/aistudio/projectdetail/4462918", style="text-decoration: underline;" target="_blank"> aistudio </a> 上使用免费的GPU体验更多案例。
                    </p>   
               </div>
               <div class="prompt">
                    <p><h4>Prompt format</h4>
                    <span> Prompt = [adjective] [object], [details], [styles or artists]. </span>
                    For more details, please refer to <a href="https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#四-prompt-指南" style="text-decoration: underline;" target="_blank">YouPromptMe Guide</a>.
                    There are more interesting models in PaddleHub, you can star <a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank"> PaddleHub</a> to follow.
                    Besides, you can use free GPU resourses in <a href="https://aistudio.baidu.com/aistudio/projectdetail/4462918", style="text-decoration: underline;" target="_blank"> aistudio </a> to enjoy more cases, have fun. 
                    </p>   
               </div>
               <img src="https://user-images.githubusercontent.com/22424850/187849103-074cb6d2-a9b4-49a1-b1f0-fc130049769f.png" alt="star Paddlehub" width="100%">
                 
           """
        )
        gr.Markdown(
            """
在"探索无限"的风格模式下，画作的真实风格完全可以由你的prompt来决定。下面是一些参考案例:


In "Explore infinity" style mode, how the image looks like is totally up to your prompt. Below are some cases:

### 复古未来主义风格

| ![00472_000_一只猫坐在椅子上，戴着一副墨镜,复古未来主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00472_000_一只猫坐在椅子上，戴着一副墨镜,复古未来主义风格.jpg) | ![00472_000_日落时的城市天际线,复古未来主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00472_000_日落时的城市天际线,复古未来主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,复古未来主义风格              | 日落时的城市天际线,复古未来主义风格                          |



### 粉彩朋克风格

| ![00017_004_一只猫坐在椅子上，戴着一副墨镜，粉彩朋克风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00017_004_一只猫坐在椅子上，戴着一副墨镜，粉彩朋克风格.jpg) | ![00029_001_日落时的城市天际线，粉彩朋克风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00029_001_日落时的城市天际线，粉彩朋克风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,粉彩朋克风格                  | 日落时的城市天际线,粉彩朋克风格                              |

### 史前遗迹风格

| ![00443_005_一只猫坐在椅子上，戴着一副墨镜,史前遗迹风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00443_005_一只猫坐在椅子上，戴着一副墨镜,史前遗迹风格.jpg) | ![00443_005_日落时的城市天际线,史前遗迹风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00443_005_日落时的城市天际线,史前遗迹风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,史前遗迹风格                  | 日落时的城市天际线,史前遗迹风格                              |




### 波普艺术风格

| ![00434_005_一只猫坐在椅子上，戴着一副墨镜,波普艺术风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00434_005_一只猫坐在椅子上，戴着一副墨镜,波普艺术风格.jpg) | ![00434_002_日落时的城市天际线,波普艺术风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00434_002_日落时的城市天际线,波普艺术风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,波普艺术风格                  | 日落时的城市天际线,后世界末日风格                            |



### 迷幻风格

| ![00451_000_一只猫坐在椅子上，戴着一副墨镜,迷幻药风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00451_000_一只猫坐在椅子上，戴着一副墨镜,迷幻药风格.jpg) | ![00451_001_日落时的城市天际线,迷幻药风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00451_001_日落时的城市天际线,迷幻药风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,迷幻风格                      | 日落时的城市天际线,迷幻风格                                  |


### 赛博朋克风格

| ![00142_003_一只猫坐在椅子上，戴着一副墨镜,赛博朋克风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00142_003_一只猫坐在椅子上，戴着一副墨镜,赛博朋克风格.jpg) | ![00142_000_日落时的城市天际线,赛博朋克风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00142_000_日落时的城市天际线,赛博朋克风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,赛博朋克风格                  | 日落时的城市天际线,赛博朋克风格                              |


### 纸箱风格


| ![00081_000_一只猫坐在椅子上，戴着一副墨镜,纸箱风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00081_000_一只猫坐在椅子上，戴着一副墨镜,纸箱风格.jpg) | ![00081_000_日落时的城市天际线,纸箱风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00081_000_日落时的城市天际线,纸箱风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,纸箱风格                      | 日落时的城市天际线,纸箱风格                                  |

### 未来主义风格

| ![00083_000_一只猫坐在椅子上，戴着一副墨镜,未来主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00083_000_一只猫坐在椅子上，戴着一副墨镜,未来主义风格.jpg) | ![00083_002_日落时的城市天际线,未来主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00083_002_日落时的城市天际线,未来主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,未来主义风格                  | 一只猫坐在椅子上，戴着一副墨镜,未来主义风格                  |



###  抽象技术风格

| ![00000_003_一只猫坐在椅子上，戴着一副墨镜, 抽象技术风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00000_003_一只猫坐在椅子上，戴着一副墨镜,抽象技术风格.jpg) | ![00000_004_日落时的城市天际线,抽象技术风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00000_004_日落时的城市天际线,抽象技术风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,抽象技术风格                  | 日落时的城市天际线,抽象技术风格                              |




### 海滩兔风格


| ![00049_001_一只猫坐在椅子上，戴着一副墨镜,海滩兔风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00049_001_一只猫坐在椅子上，戴着一副墨镜,海滩兔风格.jpg) | ![00049_003_日落时的城市天际线,海滩兔风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00049_003_日落时的城市天际线,海滩兔风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,海滩兔风格                    | 日落时的城市天际线,海滩兔风格                                |


### 粉红公主风格

| ![00038_004_一只猫坐在椅子上，戴着一副墨镜，粉红公主风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00038_004_一只猫坐在椅子上，戴着一副墨镜，粉红公主风格.jpg) | ![00046_004_日落时的城市天际线，粉红公主风格-1](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00046_004_日落时的城市天际线，粉红公主风格-1.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,粉红公主风格                  | 日落时的城市天际线,粉红公主风格                              |


### 嬉皮士风格

| ![00275_002_一只猫坐在椅子上，戴着一副墨镜,嬉皮士风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00275_002_一只猫坐在椅子上，戴着一副墨镜,嬉皮士风格.jpg) | ![00275_001_日落时的城市天际线,嬉皮士风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00275_001_日落时的城市天际线,嬉皮士风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,嬉皮士风格                    | 日落时的城市天际线,嬉皮士风格                                |

### 幻象之城风格

| ![00288_000_一只猫坐在椅子上，戴着一副墨镜,幻象之城风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00288_000_一只猫坐在椅子上，戴着一副墨镜,幻象之城风格.jpg) | ![00288_004_日落时的城市天际线,幻象之城风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00288_004_日落时的城市天际线,幻象之城风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,幻象之城风格                  | 日落时的城市天际线,幻象之城风格                              |


### 美人鱼风格

| ![00351_002_一只猫坐在椅子上，戴着一副墨镜,美人鱼风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00351_002_一只猫坐在椅子上，戴着一副墨镜,美人鱼风格.jpg) | ![00351_000_日落时的城市天际线,美人鱼风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00351_000_日落时的城市天际线,美人鱼风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,美人鱼风格                    | 日落时的城市天际线,美人鱼风格                                |


### 迷宫物语风格


| ![00382_005_一只猫坐在椅子上，戴着一副墨镜,迷宫物语风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00382_005_一只猫坐在椅子上，戴着一副墨镜,迷宫物语风格.jpg) | ![00382_000_日落时的城市天际线,迷宫物语风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00382_000_日落时的城市天际线,迷宫物语风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,迷宫物语风格                  | 日落时的城市天际线,迷宫物语风格                              |

### 仙女风格


| ![00397_003_一只猫坐在椅子上，戴着一副墨镜,仙女风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00397_003_一只猫坐在椅子上，戴着一副墨镜,仙女风格.jpg) | ![00397_004_日落时的城市天际线,仙女风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00397_004_日落时的城市天际线,仙女风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,仙女风格                      | 日落时的城市天际线,仙女风格                                  |





### Low Poly 风格

| ![猫low-poly风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/猫low-poly风格.jpg) | ![sky-line-low-poly](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/sky-line-low-poly.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜, low poly 风格                | 日落时的城市天际线, low-poly                                 |




### 浮世绘风格

| ![00564_001_一只猫坐在椅子上，戴着一副墨镜,浮世绘风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00564_001_一只猫坐在椅子上，戴着一副墨镜,浮世绘风格.jpg) | ![00564_002_日落时的城市天际线,浮世绘风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00564_002_日落时的城市天际线,浮世绘风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,浮世绘风格                    | 日落时的城市天际线,浮世绘风格                                |

### 矢量心风格

| ![00573_001_一只猫坐在椅子上，戴着一副墨镜,矢量心风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00573_001_一只猫坐在椅子上，戴着一副墨镜,矢量心风格.jpg) | ![00573_005_日落时的城市天际线,矢量心风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00573_005_日落时的城市天际线,矢量心风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,矢量心风格                    | 日落时的城市天际线,矢量心风格                                |


### 摩托车手风格


| ![00051_000_一只猫坐在椅子上，戴着一副墨镜,摩托车手风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00051_000_一只猫坐在椅子上，戴着一副墨镜,摩托车手风格.jpg) | ![日落时的城市天际线,摩托车手风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/日落时的城市天际线,摩托车手风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,摩托车手风格                  | 日落时的城市天际线,摩托车手风格                              |



### 孟菲斯公司风格


| ![00114_001_一只猫坐在椅子上，戴着一副墨镜,孟菲斯公司风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00114_001_一只猫坐在椅子上，戴着一副墨镜,孟菲斯公司风格.jpg) | ![00114_002_日落时的城市天际线,孟菲斯公司风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00114_002_日落时的城市天际线,孟菲斯公司风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,孟菲斯公司风格                | 日落时的城市天际线,孟菲斯公司风格                            |


### 泥塑风格


| ![一只猫坐在椅子上，戴着一副墨镜, 泥塑风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/一只猫坐在椅子上戴着一副墨镜泥塑风格.jpg) | ![00013_002_日落时的城市天际线, 泥塑](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00013_002_日落时的城市天际线,泥塑.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜, 泥塑风格                     | 日落时的城市天际线, 泥塑风格                                 |




### 苔藓风格

| ![00006_001_一只猫坐在椅子上，戴着一副墨镜，苔藓风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00006_001_一只猫坐在椅子上，戴着一副墨镜，苔藓风格.jpg) | ![00004_004_日落时的城市天际线，苔藓风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00004_004_日落时的城市天际线，苔藓风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,苔藓风格                      | 日落时的城市天际线,苔藓风格                                  |



### 新浪潮风格

| ![00389_000_一只猫坐在椅子上，戴着一副墨镜,新浪潮风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00389_000_一只猫坐在椅子上，戴着一副墨镜,新浪潮风格.jpg) | ![00389_005_日落时的城市天际线,新浪潮风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00389_005_日落时的城市天际线,新浪潮风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,新浪潮风格                    | 日落时的城市天际线,新浪潮风格                                |

### 嘻哈风格

| ![00274_000_一只猫坐在椅子上，戴着一副墨镜,嘻哈风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00274_000_一只猫坐在椅子上，戴着一副墨镜,嘻哈风格.jpg) | ![00274_005_日落时的城市天际线,嘻哈风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00274_005_日落时的城市天际线,嘻哈风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,嘻哈风格                      | 日落时的城市天际线,嘻哈风格                                  |

### 矢量图

| ![00177_001_一只猫坐在椅子上，戴着一副墨镜, 矢量图](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00177_001_一只猫坐在椅子上戴着一副墨镜矢量图.jpg) | ![00020_002_日落时的城市天际线, 矢量图](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00020_002_日落时的城市天际线矢量图.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜, 矢量图                       | 日落时的城市天际线, 矢量图                                   |

### 铅笔艺术


| ![00203_000_一只猫坐在椅子上，戴着一副墨镜, 铅笔艺术](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00203_000_一只猫坐在椅子上戴着一副墨镜铅笔艺术.jpg) | ![00053_000_日落时的城市天际线, 铅笔艺术](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00053_000_日落时的城市天际线铅笔艺术.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜, 铅笔艺术                     | 日落时的城市天际线, 铅笔艺术                                 |


###  女巫店风格

| ![00606_001_一只猫坐在椅子上，戴着一副墨镜,女巫店风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00606_001_一只猫坐在椅子上，戴着一副墨镜,女巫店风格.jpg) | ![00606_000_日落时的城市天际线,女巫店风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00606_000_日落时的城市天际线,女巫店风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,女巫店风格                    | 日落时的城市天际线,女巫店风格                                |



### 4D 建模


| ![00230_000_一只猫坐在椅子上，戴着一副墨镜, 4D 建模](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00230_000_一只猫坐在椅子上戴着一副墨镜4D建模.jpg) | ![00082_001_日落时的城市天际线, 4D 建模](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00082_001_日落时的城市天际线4D建模.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜, 4D 建模                      | 日落时的城市天际线, 4D 建模                                  |



### 水彩墨风格


| ![00280_004_一只猫坐在椅子上，戴着一副墨镜, 水彩墨风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00280_004_一只猫坐在椅子上，戴着一副墨镜,水彩墨风格.jpg) | ![00130_004_日落时的城市天际线, 水彩墨风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00130_004_日落时的城市天际线,水彩墨风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜, 水彩墨风格                   | 日落时的城市天际线, 水彩墨风格                               |



###  酸性精灵风格

| ![00001_004_一只猫坐在椅子上，戴着一副墨镜,酸性精灵风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00001_004_一只猫坐在椅子上，戴着一副墨镜,酸性精灵风格.jpg) | ![00001_004_日落时的城市天际线,酸性精灵风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00001_004_日落时的城市天际线,酸性精灵风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,酸性精灵风格                  | 日落时的城市天际线,酸性精灵风格                              |


### 海盗风格

| ![00427_002_一只猫坐在椅子上，戴着一副墨镜,海盗风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00427_002_一只猫坐在椅子上，戴着一副墨镜,海盗风格.jpg) | ![00427_000_日落时的城市天际线,海盗风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00427_000_日落时的城市天际线,海盗风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 日落时的城市天际线,海盗风格                                  | 一只猫坐在椅子上，戴着一副墨镜,海盗风格                      |



### 古埃及风格


| ![00017_005_一只猫坐在椅子上，戴着一副墨镜,古埃及风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00017_005_一只猫坐在椅子上，戴着一副墨镜,古埃及风格.jpg) | ![00017_003_日落时的城市天际线,古埃及风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00017_003_日落时的城市天际线,古埃及风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,古埃及风格                    | 日落时的城市天际线,古埃及风格                                |

### 风帽风格


| ![戴着帽子的猫](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/戴着帽子的猫.jpg) | ![戴着帽子的城市](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/戴着帽子的城市.jpg) |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,风帽风格                   | 日落时的城市天际线,风帽风格                                  |

### 装饰艺术风格


| ![00029_000_一只猫坐在椅子上，戴着一副墨镜,装饰艺术风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00029_000_一只猫坐在椅子上，戴着一副墨镜,装饰艺术风格.jpg) | ![00029_005_日落时的城市天际线,装饰艺术风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00029_005_日落时的城市天际线,装饰艺术风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,装饰艺术风格                  | 日落时的城市天际线,装饰艺术风格                              |

### 极光风格


| ![00035_004_一只猫坐在椅子上，戴着一副墨镜,极光风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00035_004_一只猫坐在椅子上，戴着一副墨镜,极光风格.jpg) | ![00035_003_日落时的城市天际线,极光风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00035_003_日落时的城市天际线,极光风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,极光风格                      | 日落时的城市天际线,极光风格                                  |

###  秋天风格


| ![00036_005_一只猫坐在椅子上，戴着一副墨镜,秋天风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00036_005_一只猫坐在椅子上，戴着一副墨镜,秋天风格.jpg) | ![00036_003_日落时的城市天际线,秋天风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00036_003_日落时的城市天际线,秋天风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 日落时的城市天际线,秋天风格                                  | 一只猫坐在椅子上，戴着一副墨镜,秋天风格                      |

### 巴洛克风格


| ![00046_002_一只猫坐在椅子上，戴着一副墨镜,巴洛克风格风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00046_002_一只猫坐在椅子上，戴着一副墨镜,巴洛克风格风格.jpg) | ![00046_003_日落时的城市天际线,巴洛克风格风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00046_003_日落时的城市天际线,巴洛克风格风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,巴洛克风格                    | 日落时的城市天际线,巴洛克风格                                |

### 立体主义风格

| ![00128_002_一只猫坐在椅子上，戴着一副墨镜,立体主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00128_002_一只猫坐在椅子上，戴着一副墨镜,立体主义风格.jpg) | ![00128_004_日落时的城市天际线,立体主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00128_004_日落时的城市天际线,立体主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,立体主义风格                  | 日落时的城市天际线,立体主义风格                              |


### 黑暗自然主义风格

| ![00147_002_一只猫坐在椅子上，戴着一副墨镜,黑暗自然主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00147_002_一只猫坐在椅子上，戴着一副墨镜,黑暗自然主义风格.jpg) | ![00147_004_日落时的城市天际线,黑暗自然主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00147_004_日落时的城市天际线,黑暗自然主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,黑暗自然主义风格              | 日落时的城市天际线,黑暗自然主义风格                          |

### 表现主义风格

| ![00190_001_一只猫坐在椅子上，戴着一副墨镜,表现主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00190_001_一只猫坐在椅子上，戴着一副墨镜,表现主义风格.jpg) | ![00190_000_日落时的城市天际线,表现主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00190_000_日落时的城市天际线,表现主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,表现主义风格                  | 日落时的城市天际线,表现主义风格                              |

### 野兽派风格

| ![00200_000_一只猫坐在椅子上，戴着一副墨镜,野兽派风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00200_000_一只猫坐在椅子上，戴着一副墨镜,野兽派风格.jpg) | ![00200_002_日落时的城市天际线,野兽派风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00200_002_日落时的城市天际线,野兽派风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,野兽派风格                    | 日落时的城市天际线,野兽派风格                                |

### 鬼魂风格

| ![00226_001_一只猫坐在椅子上，戴着一副墨镜,鬼魂风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00226_001_一只猫坐在椅子上，戴着一副墨镜,鬼魂风格.jpg) | ![00226_002_日落时的城市天际线,鬼魂风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00226_002_日落时的城市天际线,鬼魂风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,鬼魂风格                      | 日落时的城市天际线,鬼魂风格                                  |

### 印象主义风格

| ![00289_000_一只猫坐在椅子上，戴着一副墨镜,印象主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00289_000_一只猫坐在椅子上，戴着一副墨镜,印象主义风格.jpg) | ![00289_001_日落时的城市天际线,印象主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00289_001_日落时的城市天际线,印象主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,印象主义风格                  | 日落时的城市天际线,印象主义风格                              |

### 卡瓦伊风格

| ![00305_001_一只猫坐在椅子上，戴着一副墨镜,卡瓦伊风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00305_001_一只猫坐在椅子上，戴着一副墨镜,卡瓦伊风格.jpg) | ![00305_000_日落时的城市天际线,卡瓦伊风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00305_000_日落时的城市天际线,卡瓦伊风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,卡瓦伊风格                    | 日落时的城市天际线,卡瓦伊风格                                |

### 极简主义风格

| ![00362_004_一只猫坐在椅子上，戴着一副墨镜,极简主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00362_004_一只猫坐在椅子上，戴着一副墨镜,极简主义风格.jpg) | ![00362_002_日落时的城市天际线,极简主义风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00362_002_日落时的城市天际线,极简主义风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,极简主义风格                  | 日落时的城市天际线,极简主义风格                              |

### 水井惠郎风格

| ![00364_000_一只猫坐在椅子上，戴着一副墨镜,水井惠郎风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00364_000_一只猫坐在椅子上，戴着一副墨镜,水井惠郎风格.jpg) | ![00364_000_日落时的城市天际线,水井惠郎风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00364_000_日落时的城市天际线,水井惠郎风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,水井惠郎风格                  | 日落时的城市天际线,水井惠郎风格                              |

###  照片写实风格

| ![00423_000_一只猫坐在椅子上，戴着一副墨镜,照片写实风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00423_000_一只猫坐在椅子上，戴着一副墨镜,照片写实风格.jpg) | ![00423_002_日落时的城市天际线,照片写实风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00423_002_日落时的城市天际线,照片写实风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,照片写实风格                  | 日落时的城市天际线,照片写实风格                              |


### 像素可爱风格

| ![00428_005_一只猫坐在椅子上，戴着一副墨镜,像素可爱风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00428_005_一只猫坐在椅子上，戴着一副墨镜,像素可爱风格.jpg) | ![00428_005_日落时的城市天际线,像素可爱风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00428_005_日落时的城市天际线,像素可爱风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,像素可爱风格                  | 日落时的城市天际线,像素可爱风格                              |



### 雨天风格

| ![00067_002_一只猫坐在椅子上，戴着一副墨镜，雨天风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00067_002_一只猫坐在椅子上，戴着一副墨镜，雨天风格.jpg) | ![00050_003_日落时的城市天际线，雨天风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00050_003_日落时的城市天际线，雨天风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 日落时的城市天际线,雨天风格                                  | 一只猫坐在椅子上，戴着一副墨镜,雨天风格                      |

### 湿漉漉的风格

| ![00523_005_一只猫坐在椅子上，戴着一副墨镜,湿漉漉的风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00523_005_一只猫坐在椅子上，戴着一副墨镜,湿漉漉的风格.jpg) | ![00523_001_日落时的城市天际线,湿漉漉的风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00523_001_日落时的城市天际线,湿漉漉的风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,湿漉漉的风格                  | 日落时的城市天际线,湿漉漉的风格                              |


### 维京人风格

| ![00577_004_一只猫坐在椅子上，戴着一副墨镜,维京人风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00577_004_一只猫坐在椅子上，戴着一副墨镜,维京人风格.jpg) | ![00577_005_日落时的城市天际线,维京人风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00577_005_日落时的城市天际线,维京人风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,维京人风格                    | 日落时的城市天际线,维京人风格                                |

### 后印象主义


| ![一只猫坐在椅子上，戴着一副墨镜,风格：后印象主义](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style/一只猫坐在椅子上，戴着一副墨镜,风格：后印象主义.jpg) | ![日落时的城市天际线, 风格：后印象主义-v2](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style/日落时的城市天际线,风格：后印象主义-v2.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,风格：后印象主义              | 日落时的城市天际线, 风格：后印象主义-v2                      |

### 素人主义


| ![一只猫坐在椅子上，戴着一副墨镜,风格：素人主义](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style/一只猫坐在椅子上，戴着一副墨镜,风格：素人主义.jpg) | ![日落时的城市天际线,风格：素人艺术](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style/日落时的城市天际线,风格：素人艺术.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,风格：素人主义                | 日落时的城市天际线, 风格：素人艺术                           |



### 碎核风格


| ![00064_000_一只猫坐在椅子上，戴着一副墨镜,碎核风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00064_000_一只猫坐在椅子上，戴着一副墨镜,碎核风格.jpg) | ![00064_002_日落时的城市天际线,碎核风格](https://raw.githubusercontent.com/OleNet/YouPromptMe/gh-pages/you-prompt-me/images/art-style-1024/00064_002_日落时的城市天际线,碎核风格.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 一只猫坐在椅子上，戴着一副墨镜,碎核风格                      | 日落时的城市天际线,碎核风格                                  |

            """
        )
        gr.HTML('''
        <div class="footer">
                    <p>Model by <a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank">PaddleHub</a> and <a href="https://wenxin.baidu.com" style="text-decoration: underline;" target="_blank">文心大模型</a> - Gradio Demo by 🤗 Hugging Face
                    </p>
        </div>
        ''')

block.queue(concurrency_count=100).launch()
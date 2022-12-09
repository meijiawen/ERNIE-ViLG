import numpy as np
import gradio as gr
import paddlehub as hub


model = hub.Module(name='ernie_vilg')
language_translation_model = hub.Module(name='baidu_translate')
language_recognition_model = hub.Module(name='baidu_language_recognition')

style_list = ['古风', '油画', '水彩', '卡通', '二次元', '浮世绘', '蒸汽波艺术', 'low poly', '像素风格', '概念艺术', '未来主义', '赛博朋克', '写实风格', '洛丽塔风格', '巴洛克风格', '超现实主义', '探索无限']

tips = {"en": "Tips: The input text will be translated into Chinese for generation", 
        "jp": "ヒント: 入力テキストは生成のために中国語に翻訳されます", 
        "kor": "힌트: 입력 텍스트는 생성을 위해 중국어로 번역됩니다"}

count = 0

def translate_language(text_prompts):
    global count
    try:
        count += 1
        tips_text = None
        language_code = language_recognition_model.recognize(text_prompts)
        if language_code != 'zh':
            text_prompts = language_translation_model.translate(text_prompts, language_code, 'zh')
    except Exception as e:
        error_text = str(e)
        return {status_text:error_text, language_tips_text:gr.update(visible=False)}
    if language_code in tips:
        tips_text = tips[language_code]
    else:
        tips_text = tips['en']
    if language_code == 'zh':
        return {language_tips_text:gr.update(visible=False), translated_language:text_prompts, trigger_component: gr.update(value=count, visible=False)}
    else:
        return {language_tips_text:gr.update(visible=True, value=tips_text), translated_language:text_prompts, trigger_component:  gr.update(value=count, visible=False)}

        
def inference(text_prompts, style_indx):
  try:
    model.token = model._apply_token(model.ak, model.sk)
    style = style_list[style_indx]
    results = model.generate_image(
        text_prompts=text_prompts, style=style, visualization=False, topk=4)
  except Exception as e:
    error_text = str(e)
    return {status_text:error_text, gallery:None}
  return {status_text:'Success', gallery:results[:4]}


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
        'A cat with glasses',
        '油画(Oil painting)'
    ],
    [
        '眼鏡をかけた猫',
        '油画(Oil painting)'
    ],
    [
        '안경을 쓴 고양이',
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
        'A cat sitting on a chair, wearing a pair of sunglasses, low poly style',
        '油画(Oil painting)'
    ],
    [
        '猫が椅子に座ってサングラスをかけている、low polyスタイル',
        '油画(Oil painting)'
    ],
    [
        '고양이 한 마리가 의자에 앉아 선글라스를 끼고 low poly 스타일을 하고 있다',
        '油画(Oil painting)'
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
        'An awesome dragon made of lightning, conceptual art',
        '油画(Oil painting)'
    ],
    [
        '稲妻で作られた畏敬の念を抱かせる竜、コンセプトアート',
        '油画(Oil painting)'
    ],
    [
        '번개로 만든 경외스러운 용, 개념 예술',
        '油画(Oil painting)'
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
    ],
    [
        'Sunset, the sun falls on the clouds, the sea is rough, the scenery is filmy',
        '油画(Oil painting)'
    ],
    [
        '夕日が沈むと、雲の上に太陽の光が落ち、海面は波が荒く、風景、フィルム感',
        '油画(Oil painting)'
    ],
    [
        '석양이 질 때 햇빛이 구름 위에 떨어지고, 해수면의 파도가 용솟음치며, 풍경, 필름감',
        '油画(Oil painting)'
    ],
]

with block:
    gr.HTML(
        """
            <div style="text-align: center; max-width: 650px; margin: 0 auto;">
              <div
                style="
                  display: inline-flex;
                  gap: 0.8rem;
                  font-size: 1.75rem;
                  margin-bottom: 10px;
                  margin-left: 220px;
                  justify-content: center;
                "
              >
              <a href="https://github.com/PaddlePaddle/PaddleHub"><img src="https://user-images.githubusercontent.com/22424850/187387422-f6c9ccab-7fda-416e-a24d-7d6084c46f67.jpg" alt="Paddlehub" width="40%"></a>
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
              <a href="https://github.com/PaddlePaddle/PaddleHub"><h1 style="font-weight: 900; margin-bottom: 7px;">
                  ERNIE-ViLG Demo
              </h1></a>
              </div> 
              <p style="margin-bottom: 10px; font-size: 94%">
                ERNIE-ViLG 2.0 is a state-of-the-art text-to-image model that generates
                images from Chinese text.
              </p>
              <a href="https://github.com/PaddlePaddle/PaddleHub"><img src="https://user-images.githubusercontent.com/22424850/188184795-98605a22-9af2-4106-827b-e58548f8892f.png" alt="star Paddlehub" width="100%"></a>
            </div>
        """
    )
    with gr.Group():
        with gr.Box():
            with gr.Row().style(mobile_collapse=False, equal_height=True):
                text = gr.Textbox(
                    label="Prompt",
                    show_label=False,
                    max_lines=1,
                    placeholder="Enter your prompt, multiple languages are supported now.",
                ).style(
                    border=(True, False, True, True),
                    rounded=(True, False, False, True),
                    container=False,
                )

                btn = gr.Button("Generate image").style(
                    margin=False,
                    rounded=(False, True, True, False),
                )
        language_tips_text = gr.Textbox(label="language tips", show_label=False, visible=False, max_lines=1)
        styles = gr.Dropdown(label="风格(style)", choices=['古风(Ancient Style)', '油画(Oil painting)', '水彩(Watercolor)', 
        '卡通(Cartoon)', '二次元(Anime)', '浮世绘(Ukiyoe)', '蒸汽波艺术(Vaporwave)', 'low poly', 
        '像素风格(Pixel Style)', '概念艺术(Conceptual Art)', '未来主义(Futurism)', '赛博朋克(Cyberpunk)', '写实风格(Realistic style)', 
        '洛丽塔风格(Lolita style)', '巴洛克风格(Baroque style)', '超现实主义(Surrealism)', '探索无限(Explore infinity)'], value='探索无限(Explore infinity)', type="index")
        gallery = gr.Gallery(
            label="Generated images", show_label=False, elem_id="gallery"
        ).style(grid=[1, 4], height="auto")
        status_text = gr.Textbox(
            label="处理状态(Process status)",
            show_label=True,
            max_lines=1,
            interactive=False
        )
        trigger_component = gr.Textbox(vaule="", visible=False) # This component is used for triggering inference funtion.
        translated_language = gr.Textbox(vaule="", visible=False)
        
        ex = gr.Examples(examples=examples, fn=translate_language, inputs=[text], outputs=[language_tips_text, status_text, trigger_component, translated_language], cache_examples=False)
        ex.dataset.headers = [""]

        
        text.submit(translate_language, inputs=[text], outputs=[language_tips_text, status_text, trigger_component, translated_language])
        btn.click(translate_language, inputs=[text], outputs=[language_tips_text, status_text, trigger_component, translated_language])
        trigger_component.change(fn=inference, inputs=[translated_language, styles], outputs=[status_text, gallery])
        gr.HTML(
            """
                <div class="prompt">
                    <p><h4>Prompt公式</h4>
                    <span> Prompt = 图片主体，细节词，修饰词 </span>
                    关于各部分的构造方式和效果，可以参考<a href="https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#四-prompt-指南" style="text-decoration: underline;" target="_blank">YouPromptMe指南</a>。
                    更多的模型，请关注<a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank"> PaddleHub 官方Repo </a>， 如果你觉得不错，请star收藏吧。
                    <p><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="90" height="20"><style>a:hover #llink{fill:url(#b);stroke:#ccc}a:hover #rlink{fill:#4183c4}</style><linearGradient id="a" x2="0" y2="100%"><stop offset="0" stop-color="#fcfcfc" stop-opacity="0"/><stop offset="1" stop-opacity=".1"/></linearGradient><linearGradient id="b" x2="0" y2="100%"><stop offset="0" stop-color="#ccc" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient><g stroke="#d5d5d5"><rect stroke="none" fill="#fcfcfc" x="0.5" y="0.5" width="54" height="19" rx="2"/><rect x="60.5" y="0.5" width="29" height="19" rx="2" fill="#fafafa"/><rect x="60" y="7.5" width="0.5" height="5" stroke="#fafafa"/><path d="M60.5 6.5 l-3 3v1 l3 3" stroke="d5d5d5" fill="#fafafa"/></g><image x="5" y="3" width="14" height="14" xlink:href="data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMTgxNzE3IiByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+R2l0SHViPC90aXRsZT48cGF0aCBkPSJNMTIgLjI5N2MtNi42MyAwLTEyIDUuMzczLTEyIDEyIDAgNS4zMDMgMy40MzggOS44IDguMjA1IDExLjM4NS42LjExMy44Mi0uMjU4LjgyLS41NzcgMC0uMjg1LS4wMS0xLjA0LS4wMTUtMi4wNC0zLjMzOC43MjQtNC4wNDItMS42MS00LjA0Mi0xLjYxQzQuNDIyIDE4LjA3IDMuNjMzIDE3LjcgMy42MzMgMTcuN2MtMS4wODctLjc0NC4wODQtLjcyOS4wODQtLjcyOSAxLjIwNS4wODQgMS44MzggMS4yMzYgMS44MzggMS4yMzYgMS4wNyAxLjgzNSAyLjgwOSAxLjMwNSAzLjQ5NS45OTguMTA4LS43NzYuNDE3LTEuMzA1Ljc2LTEuNjA1LTIuNjY1LS4zLTUuNDY2LTEuMzMyLTUuNDY2LTUuOTMgMC0xLjMxLjQ2NS0yLjM4IDEuMjM1LTMuMjItLjEzNS0uMzAzLS41NC0xLjUyMy4xMDUtMy4xNzYgMCAwIDEuMDA1LS4zMjIgMy4zIDEuMjMuOTYtLjI2NyAxLjk4LS4zOTkgMy0uNDA1IDEuMDIuMDA2IDIuMDQuMTM4IDMgLjQwNSAyLjI4LTEuNTUyIDMuMjg1LTEuMjMgMy4yODUtMS4yMy42NDUgMS42NTMuMjQgMi44NzMuMTIgMy4xNzYuNzY1Ljg0IDEuMjMgMS45MSAxLjIzIDMuMjIgMCA0LjYxLTIuODA1IDUuNjI1LTUuNDc1IDUuOTIuNDIuMzYuODEgMS4wOTYuODEgMi4yMiAwIDEuNjA2LS4wMTUgMi44OTYtLjAxNSAzLjI4NiAwIC4zMTUuMjEuNjkuODI1LjU3QzIwLjU2NSAyMi4wOTIgMjQgMTcuNTkyIDI0IDEyLjI5N2MwLTYuNjI3LTUuMzczLTEyLTEyLTEyIi8+PC9zdmc+"/><g aria-hidden="false" fill="#333" text-anchor="middle" font-family="Helvetica Neue,Helvetica,Arial,sans-serif" text-rendering="geometricPrecision" font-weight="700" font-size="110px" line-height="14px"><a target="_blank" xlink:href="https://github.com/PaddlePaddle/PaddleHub"><text aria-hidden="true" x="355" y="150" fill="#fff" transform="scale(.1)" textLength="270">Stars</text><text x="355" y="140" transform="scale(.1)" textLength="270">Stars</text><rect id="llink" stroke="#d5d5d5" fill="url(#a)" x=".5" y=".5" width="54" height="19" rx="2"/></a><a target="_blank" xlink:href="https://github.com/PaddlePaddle/PaddleHub/stargazers"><rect width="30" x="60" height="20" fill="rgba(0,0,0,0)"/><text aria-hidden="true" x="745" y="150" fill="#fff" transform="scale(.1)" textLength="210">8.4k</text><text id="rlink" x="745" y="140" transform="scale(.1)" textLength="210">8.4k</text></a></g></svg></p>
                    同时，可以在 <a href="https://aistudio.baidu.com/aistudio/projectdetail/4462918", style="text-decoration: underline;" target="_blank"> aistudio </a> 上使用免费的GPU体验更多案例。
                    </p>   
               </div>
               <div class="prompt">
                    <p><h4>Prompt format</h4>
                    <span> Prompt = object, details, description </span>
                    For more details, please refer to <a href="https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#四-prompt-指南" style="text-decoration: underline;" target="_blank">YouPromptMe Guide</a>.
                    There are more interesting models in PaddleHub, if you think it's great, welcome to star <a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank"> PaddleHub</a>.
                    <p><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="90" height="20"><style>a:hover #llink{fill:url(#b);stroke:#ccc}a:hover #rlink{fill:#4183c4}</style><linearGradient id="a" x2="0" y2="100%"><stop offset="0" stop-color="#fcfcfc" stop-opacity="0"/><stop offset="1" stop-opacity=".1"/></linearGradient><linearGradient id="b" x2="0" y2="100%"><stop offset="0" stop-color="#ccc" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient><g stroke="#d5d5d5"><rect stroke="none" fill="#fcfcfc" x="0.5" y="0.5" width="54" height="19" rx="2"/><rect x="60.5" y="0.5" width="29" height="19" rx="2" fill="#fafafa"/><rect x="60" y="7.5" width="0.5" height="5" stroke="#fafafa"/><path d="M60.5 6.5 l-3 3v1 l3 3" stroke="d5d5d5" fill="#fafafa"/></g><image x="5" y="3" width="14" height="14" xlink:href="data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMTgxNzE3IiByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+R2l0SHViPC90aXRsZT48cGF0aCBkPSJNMTIgLjI5N2MtNi42MyAwLTEyIDUuMzczLTEyIDEyIDAgNS4zMDMgMy40MzggOS44IDguMjA1IDExLjM4NS42LjExMy44Mi0uMjU4LjgyLS41NzcgMC0uMjg1LS4wMS0xLjA0LS4wMTUtMi4wNC0zLjMzOC43MjQtNC4wNDItMS42MS00LjA0Mi0xLjYxQzQuNDIyIDE4LjA3IDMuNjMzIDE3LjcgMy42MzMgMTcuN2MtMS4wODctLjc0NC4wODQtLjcyOS4wODQtLjcyOSAxLjIwNS4wODQgMS44MzggMS4yMzYgMS44MzggMS4yMzYgMS4wNyAxLjgzNSAyLjgwOSAxLjMwNSAzLjQ5NS45OTguMTA4LS43NzYuNDE3LTEuMzA1Ljc2LTEuNjA1LTIuNjY1LS4zLTUuNDY2LTEuMzMyLTUuNDY2LTUuOTMgMC0xLjMxLjQ2NS0yLjM4IDEuMjM1LTMuMjItLjEzNS0uMzAzLS41NC0xLjUyMy4xMDUtMy4xNzYgMCAwIDEuMDA1LS4zMjIgMy4zIDEuMjMuOTYtLjI2NyAxLjk4LS4zOTkgMy0uNDA1IDEuMDIuMDA2IDIuMDQuMTM4IDMgLjQwNSAyLjI4LTEuNTUyIDMuMjg1LTEuMjMgMy4yODUtMS4yMy42NDUgMS42NTMuMjQgMi44NzMuMTIgMy4xNzYuNzY1Ljg0IDEuMjMgMS45MSAxLjIzIDMuMjIgMCA0LjYxLTIuODA1IDUuNjI1LTUuNDc1IDUuOTIuNDIuMzYuODEgMS4wOTYuODEgMi4yMiAwIDEuNjA2LS4wMTUgMi44OTYtLjAxNSAzLjI4NiAwIC4zMTUuMjEuNjkuODI1LjU3QzIwLjU2NSAyMi4wOTIgMjQgMTcuNTkyIDI0IDEyLjI5N2MwLTYuNjI3LTUuMzczLTEyLTEyLTEyIi8+PC9zdmc+"/><g aria-hidden="false" fill="#333" text-anchor="middle" font-family="Helvetica Neue,Helvetica,Arial,sans-serif" text-rendering="geometricPrecision" font-weight="700" font-size="110px" line-height="14px"><a target="_blank" xlink:href="https://github.com/PaddlePaddle/PaddleHub"><text aria-hidden="true" x="355" y="150" fill="#fff" transform="scale(.1)" textLength="270">Stars</text><text x="355" y="140" transform="scale(.1)" textLength="270">Stars</text><rect id="llink" stroke="#d5d5d5" fill="url(#a)" x=".5" y=".5" width="54" height="19" rx="2"/></a><a target="_blank" xlink:href="https://github.com/PaddlePaddle/PaddleHub/stargazers"><rect width="30" x="60" height="20" fill="rgba(0,0,0,0)"/><text aria-hidden="true" x="745" y="150" fill="#fff" transform="scale(.1)" textLength="210">8.4k</text><text id="rlink" x="745" y="140" transform="scale(.1)" textLength="210">8.4k</text></a></g></svg></p>
                    Besides, you can use free GPU resourses in <a href="https://aistudio.baidu.com/aistudio/projectdetail/4462918", style="text-decoration: underline;" target="_blank"> aistudio </a> to enjoy more cases, have fun. 
                    </p>   
               </div>
                
           """
        )
        gr.Markdown(
            """
在"探索无限"的风格模式下，画作的真实风格完全可以由你的prompt来决定。下面是一些参考案例:

In "Explore infinity" style mode, how the image looks like is totally up to your prompt. Below are some cases:

|<img src="https://bce.bdstatic.com/doc/AIDP/wenxin/174_蒙娜丽莎，赛博朋克，宝丽来，33毫米,蒸汽波艺术_000-1_7b4a78a.png" alt="drawing" width="300"/>|
| --- | 
| prompt：蒙娜丽莎，赛博朋克，宝丽来，33毫米,</br>蒸汽波艺术  |


|<img src="https://bce.bdstatic.com/doc/AIDP/wenxin/3_72d9343.png" alt="drawing" width="300"/>|
| --- | 
| prompt：火焰，凤凰，少女，未来感，高清，3d，</br>精致面容，cg感，古风，唯美，毛发细致，上半身立绘 |


|<img src="https://bce.bdstatic.com/doc/AIDP/wenxin/4_e1f5cbb.png" alt="drawing" width="300"/>|
| --- | 
|  prompt：巨狼，飘雪，蓝色大片烟雾，毛发细致，</br>烟雾缭绕，高清，3d，cg感，侧面照  |


| <img src="https://bce.bdstatic.com/doc/AIDP/wenxin/5_d380451.png" alt="drawing" width="400"/> |
| --- | 
|  prompt：浮世绘日本科幻哑光绘画，概念艺术，</br>动漫风格神道寺禅园英雄动作序列，包豪斯| 

<img src="https://bce.bdstatic.com/doc/AIDP/wenxin/1_3612449.jpg" alt="drawing" width="600"/>               

### <u>[更多内容...](https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#四-prompt-指南)([Explore more...](https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#四-prompt-指南))</u>


            """
        )
        gr.HTML('''
        <div class="footer">
                    <p>Model by <a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank">PaddleHub</a> and <a href="https://wenxin.baidu.com/ernie-vilg" style="text-decoration: underline;" target="_blank">文心大模型</a> - Gradio Demo by 🤗 Hugging Face
                    </p>
        </div>
        ''')

block.queue(concurrency_count=128).launch()
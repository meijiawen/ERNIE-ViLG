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
                    关于各部分的构造方式和效果，可以参考<a href="https://github.com/PaddlePaddle/PaddleHub/tree/develop/modules/image/text_to_image/ernie_vilg#六-prompt-指南" style="text-decoration: underline;" target="_blank">YouPromptMe指南</a>。
                    </p>   
               </div>
                <div class="footer">
                    <p>Model by <a href="https://github.com/PaddlePaddle/PaddleHub" style="text-decoration: underline;" target="_blank">PaddleHub</a> and <a href="https://wenxin.baidu.com" style="text-decoration: underline;" target="_blank">文心大模型</a> - Gradio Demo by 🤗 Hugging Face
                    </p>
                </div>
                 
           """
        )

block.queue(concurrency_count=500).launch()
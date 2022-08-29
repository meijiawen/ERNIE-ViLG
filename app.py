import numpy as np
import gradio as gr
import paddlehub as hub


model = hub.Module(name='ernie_vilg')
    
    
def inference(text_prompts):
  results = model.generate_image(
      text_prompts=text_prompts)
  return np.array(results[0])

outputs = [
           gr.outputs.Image(type="numpy",label="result")
           ]

title="ERNIE-ViLG"

description="ERNIE-ViLG model, which supports text-to-image task."

gr.Interface(inference, gr.inputs.Textbox(),outputs,title=title,description=description).launch(enable_queue=True)
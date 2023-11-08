from h2o_wave import main, app, Q, ui, data
import asyncio


async def stream_message(q):
    stream = ''
    q.page['example'].data += [stream, False]
    # Show the "Stop generating" button
    q.page['example'].generating = True
    for w in 'I am a fake chatbot. Sorry, I cannot help you.'.split():
        await asyncio.sleep(0.3)
        stream += w + ' '
        q.page['example'].data[-1] = [stream, False]
        await q.page.save()
    # Hide the "Stop generating" button
    q.page['example'].generating = False
    await q.page.save()
html = '''
<style>
.anim {
  font-weight: 900;
  font-size: 3.5em;
  color: #F1C40F;
}
.anim .letter {
  display: inline-block;
  line-height: 1em;
}
</style>

<h1 id="animation" class="anim">Welcome to Machine Learning Studio!</h1>
'''

script = '''
// Wrap every letter in a span
var textWrapper = document.querySelector('.anim');
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: true})
  .add({
    targets: '.anim .letter',
    scale: [4,1],
    opacity: [0,1],
    translateZ: 0,
    easing: "easeOutExpo",
    duration: 950,
    delay: (el, i) => 70*i
  }).add({
    targets: '.anim',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 10000000
  });
'''

# Add a placeholder for the animation.





@app('/main')
async def serve(q: Q):
    if not q.client.initialized:
        q.page['header'] = ui.header_card(
            box='1 1 12 1',
            title='My app',
            subtitle='My app subtitle',
            image='https://wave.h2o.ai/img/h2o-logo.svg',
            items=[
                ui.links(inline=True, items=[
                    ui.link(label='Data Analyzer', path='/dataAnalyzer', target='_blank'),
                    ui.link(label='Model Analyzer', path='/modelAnalyzer', target='_blank'),
                    ui.link(label='docs', path='https://www.h2o.ai/', target='_blank'),
                ])
            ]
        )
        q.page['banner'] = ui.meta_card(
        box='',
        # Load anime.js
        scripts=[ui.script(path='https://cdnjs.cloudflare.com/ajax/libs/animejs/2.0.2/anime.min.js')],
        script=ui.inline_script(
            # The Javascript code for this script.
            content=script,
            # Execute this script only if the 'anime' library is available.
            requires=['anime'],
            # Execute this script only if the 'animation' element is available.
            targets=['animation'],
        ))
        q.page['banner_1'] = ui.markup_card(
            box='1 2 12 12',
            title='',
            content=html,
        )

    # Handle the stop event.
    # A new message arrived.

    await q.page.save()
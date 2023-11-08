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
  color: #e8500d;
}
.anim .letter {
  display: inline-block;
  line-height: 1em;
}
</style>

<h1 id="animation" class="anim">Be Aware Legally!</h1>
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





@app('/demo')
async def serve(q: Q):
    if not q.client.initialized:
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
            box='1 1 12 12',
            title='Legal Aware Chat Bot',
            content=html,
        )
        q.page['example'] = ui.chatbot_card(
            box='1 3 12 8',
            data=data(fields='content from_user', t='list'),
            name='chatbot',
            events=['stop']
        )
        q.client.initialized = True

    # Handle the stop event.
    if q.events.chatbot and q.events.chatbot.stop:
        # Cancel the streaming task.
        q.client.task.cancel()
        # Hide the "Stop generating" button.
        q.page['example'].generating = False
    # A new message arrived.
    elif q.args.chatbot:
        # Append user message.
        q.page['example'].data += [q.args.chatbot, True]
        # Run the streaming within cancelable asyncio task.
        q.client.task = asyncio.create_task(stream_message(q))

    await q.page.save()
from h2o_wave import main, app, Q, ui
import pandas as pd
import io
import os

class Data:
    def __init__(self, data):
        self.data = data


def DisplayData(df,q):
    q.client.form_count = 5
    q.page[f'table{q.client.form_count}'] = ui.form_card(box=f'1 {q.client.form_count} 12 6', items=[
            # modify heading here (content)
            ui.text_xl(content='Df.head(5)'),
            ui.table(
                name='table',
                columns=[ui.table_column(name=i, label=i, min_width='200',cell_type=ui.markdown_table_cell_type(target='_blank')) for i in df.columns],
                height='450px',
                rows=[ui.table_row(name=f'row{i}', cells=list(str(i) for i in df.values[i])) for i in range(5)],
            )
    ])
    q.client.form_count += 6
    


@app('/demo')
async def serve(q: Q):
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
    links = q.args.user_files
    if links:
        items = [ui.text_xl('Files uploaded!')]
        for link in links:
            local_path = await q.site.download(link, '.')
            #
            # The file is now available locally; process the file.
            # To keep this example simple, we just read the file size.
            #
            size = os.path.getsize(local_path)
            #print(pd.read_csv(local_path))
            DisplayData(pd.read_csv(local_path),q)  

            items.append(ui.link(label=f'{os.path.basename(link)} ({size} bytes)', download=True, path=link))
            # Clean up
            os.remove(local_path)

        items.append(ui.button(name='back', label='Back', primary=True))
        q.page['example'].items = items
    else:
        q.page['example'] = ui.form_card(box='1 2 12 5', items=[
            ui.text_xl('Upload some files'),
            ui.file_upload(name='user_files', label='Upload', multiple=True),
        ])
    await q.page.save()
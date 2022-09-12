import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.db import connect
from prodigy.util import get_hash


@prodigy.recipe(
    "transformation_manual",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str)
)

def transformation_manual(dataset: str, source: str):

    HTML_TEMPLATE = """<p><b>Sentence:</b><br>{{text}}</p><p><br></p><input key="{{_task_hash}}" type="radio" id="t" name="transformation" value="Transformation" onclick="(function(rb_object){window.prodigy.update({ [rb_object.name]: rb_object.id }); document.querySelector('.prodigy-options').style.display = 'block';})(this)"><label for="t"> Transformation    </label><input type="radio" id="nt" name="transformation" value="No Transformation" onclick="(function(rb_object){window.prodigy.update({ [rb_object.name]: rb_object.id }); document.querySelector('.prodigy-options').style.display = 'none'; for (const x of document.querySelectorAll('.prodigy-option')) {if (x.children[0].checked == true){x.click()}};})(this)"><label for="nt"> No Transformation    </label><input type="radio" id="dk" name="transformation" value="Don't know" onclick="(function(rb_object){window.prodigy.update({ [rb_object.name]: rb_object.id }); document.querySelector('.prodigy-options').style.display = 'none';for (const x of document.querySelectorAll('.prodigy-option')) {if (x.children[0].checked == true){x.click()}};})(this)"><label for="dk"> Don't Know</label> """

    JAVASCRIPT = """
    document.addEventListener('prodigymount', () => {
        const transformations = document.querySelector('.prodigy-options')
        transformations.style.display="none";
        document.addEventListener('prodigyanswer', event => {
            console.log('answered!', event.detail);
            transformations.style.display="none";});
    })
    """
    
    def get_progress(ctrl, update_return_value):
        return ctrl.total_annotated / STREAM_LEN
    
    # Load the stream from a JSONL file and return a generator that yields a dictionary for each example in the data
    stream = JSONL(source)
    stream = list(add_options(stream))
    STREAM_LEN = len(stream)

    # Remove already annotated samples
    db = connect()
    stream = [x for x in stream if get_hash(x, ['text']) not in db.get_input_hashes(dataset)]

    blocks = [
        {"view_id": "html", "html_template": HTML_TEMPLATE},
        {"view_id": "choice", "text": None}
    ]

    return {
        "view_id": "blocks",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "config": {
            "choice_style": "multiple",
            "blocks": blocks,
            "javascript": JAVASCRIPT,
        },
        "progress": get_progress
    }

def add_options(stream):
    # Helper function to add options to every task in a stream
    options = [
        {"id": "portfolio", "text": "Portfolio Transformation"},
        {"id": "organizational", "text": "Organizational Transformation"},
        {"id": "financial", "text": "Financial Transformation"},
        {"id": "dontknow", "text": "Don't Know"},
    ]
    for task in stream:
        task["options"] = options
        yield task
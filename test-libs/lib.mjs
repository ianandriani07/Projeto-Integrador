
processor = new Processor();

let elements = document.getElementsByTagName('input');
let form = document.getElementById("formula");
form.addEventListener('change', () => {
    let out = processor.exec(form.value);
    output.textContent = out.toString();
});

let output = document.getElementById('output');

for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener('change', () => {
        const el = elements[i];
        processor.addVariable(el.id, el.value);

        let out = processor.exec(form.value);
        output.textContent = out.toString();
    });
}

let formula = {};
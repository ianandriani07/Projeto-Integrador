function se(condition, on_true, on_false) {
    if (eval(condition)) {
        return eval(on_true);
    } else if (on_false != undefined) {
        return eval(on_false);
    }
    return 0;
}


function replace_variables(variables, formula) {
    let out = formula;
    variables.forEach((variable) => {
        out = out.replaceAll(variable, `world_obj.${variable}`);
    }
    );
    return out;
}

function execute_formula(reference, formula) {
    const variables = Object.keys(reference);

    if (variables.length == 0 || !formula) {
        return 0;
    }

    try {
        return eval(replace_variables(variables, formula));
    } catch {
        return 0;
    }
}

let elements = document.getElementsByTagName('input');
let form = document.getElementById("formula");
form.addEventListener('change', () => {
    let out = execute_formula(world_obj, form.value);
    output.textContent = out.toString();
});

let output = document.getElementById('output');

for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener('change', () => {
        const el = elements[i];
        world_obj[el.id] = parseInt(el.value);

        let out = execute_formula(world_obj, form.value);
        output.textContent = out.toString();
    });
}

let world_obj = {};
let formula = {};
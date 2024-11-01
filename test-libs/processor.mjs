const seRegexes = {
    'equal': /((?:\W+|^)se\(.+?)\=+(.+?,.+?\))/g,
    'or': /((?:\W+|^)se\(.+?)ou(.+?,.+?\))/g,
    'and': /((?:\W+|^)se\(.+?)e(.+?,.+?\))/g,
    'seReplace': /(\W+|^)se(\(.+?\))/g
};

const preProcessor = [(formula) => {
    formula = formula.replace(seRegexes.equal, "$1==$2").replace(seRegexes.or, "$1||$2").replace(seRegexes.and, "$1&&$2")
        .replace(seRegexes.seReplace, "$1DefaultFunctions.se$2");
    return formula;
}];

class DefaultFunctions {
    static se(condition, on_true, on_false) {
        if (condition) {
            return on_true;
        } else if (on_false != undefined) {
            return on_false;
        }

        return 0;
    }
}

class Processor {

    static #preProcess(formula) {
        preProcessor.forEach((func) => {
            formula = func(formula);
        });

        return formula;
    }

    static #replace_variables(variables, formula) {
        let out = formula;
        variables.forEach((variable) => {
            out = out.replaceAll(variable, `world_obj.${variable}`);
        }
        );
        return out;
    }

    #convertValueToString(variable, value) {
        if (variable in this.conversion_table) {
            return this.conversion_table[variable][value];
        }

        let output = parseInt(value);
        if (isNaN(output)) {
            return 0;
        }

        return output;
    }

    constructor() {
        this.variables = {};
        this.conversion_table = {};
    }

    addVariable(variable, value) {
        if (typeof value === 'string') {
            this.variables[variable] = this.#convertValueToString(variable, value);
        } else if (typeof value === 'number') {
            this.variables[variable] = value;
        } else {
            console.warn(`Unexpected variable ${typeof value} passed! It must be either 'string' or 'number'`);
            this.variables[variable] = 0;
        }
    }

    clearVariables() {
        this.variables = {};
    }


    addTable(table) {
        Object.assign(this.conversion_table, table);
    }

    clearTables() {
        this.conversion_table = {};
    }

    reset() {
        this.clearVariables();
        this.clearTables();
    }

    exec(formula) {
        formula = formula.replaceAll(' ', '');
        const variables_name = Object.keys(this.variables);

        if (variables_name.length == 0 || !formula) {
            return 0;
        }

        formula = Processor.#preProcess(formula);
        console.log(formula);

        try {
            const world_obj = this.variables;
            return eval(Processor.#replace_variables(variables_name, formula));
        } catch {
            return 0;
        }
    }
}
/**
 * Creates a new component from *baseComponent* with the *defaults* prop defaults.
 */
export function createComponent(baseComponent, defaults) {
    return (props) => {
        return baseComponent({...defaults, ...props});
    };
}
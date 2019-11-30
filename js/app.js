var cl = console.log
const app_container = document.getElementById('app_container')

class Image  extends React.Component {
    render() {
        return (
            <h1>Image</h1>
        )
    }
}

class TextHistory  extends React.Component {
    render() {
        return (
           <div>

           </div>
            )
    }
}
class Text  extends React.Component {
    render() {
        return (
            <div>
                <h1>Text</h1>
                <form>
                   <textarea></textarea>
                   <input type="submit"></input>
                </form>
                <TextHistory/>
            </div>
        )
    }
}

class App extends React.Component {
    render() {
        return (
        <div>
           <Image/>
           <Text/>
        </div>   
        )
    }
}

ReactDOM.render(
    <App/>,
    app_container
);

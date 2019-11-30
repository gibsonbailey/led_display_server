var cl = console.log
const app_container = document.getElementById('app_container')

class Image  extends React.Component {
    render() {
        return (
            <h1>Image</h1>
        )
    }
}

class TextCommit  extends React.Component {
    render() {
        return (
            <div>
                <p>{this.props.text}</p>
                <p>{this.props.date}</p>
            </div>
        )
    }
}


class TextHistory  extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            history: [
                {
                    id: 1,
                    text: 'hello, I am an alien.',
                    date: '01-20-2018',
                },{
                    id: 2,
                    text: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.',
                    date: '01-20-2018',
                },{
                    id: 3,
                    text: 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga.',
                    date: '01-20-2018',
                },{
                    id: 4,
                    text: 'Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. ',
                    date: '01-20-2018',
                },{
                    id: 5,
                    text: 'Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat',
                    date: '01-20-2018',
                }
            ]
        }
    }

    componentDidMount() {
        // make request for previous text uploads
    }

    render() {
        return (
           <div>
                {this.state.history.map(item => 
                    <TextCommit text={item.text} date={item.date} key={item.id} />
                )}
                <button>More</button>
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

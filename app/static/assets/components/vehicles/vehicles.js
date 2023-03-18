import { html, render, Component, useState} from '/static/assets/module/standalone.module.js';


class App extends Component {  

  state = { 
  location:null,
  category:null,
  brand:null,
  fuel:null,
  used:null,
  transmission:null,
  error:null, 
  ready:false,
  vehicles: [],
  showPagination:false,
  showLink:false, currentPage: 1, postsPerPage: 8 };
  
  urls = { get: null };
  
  
  constructor(props) {
    super(props);
    this.urls = { get:`https://alsmotors-2mlm.onrender.com/vehicles/api`};

  }

  async componentDidMount() {

    const reqOpt = { method: 'GET', mode:'cors', headers:{'Content-Type': 'application/json' } };
    const response = await fetch(this.urls.get, reqOpt).then(response => response.json())

    this.setState({ready:true});
    this.setState({vehicles:response});

  }


  render() {

    const indexOfLastPost = this.state.currentPage * this.state.postsPerPage;
    const indexOfFirstPost = indexOfLastPost - this.state.postsPerPage;
    const currentPosts = this.state.vehicles.slice(indexOfFirstPost, indexOfLastPost);

    const item_model = (items) => {
      return items.map((a) => {
        return a;
    });
   };

    //Implement page numbers
    const pageNumbers = []

    for (let i = 1; i <= Math.ceil(this.state.vehicles.length / this.state.postsPerPage); i++) {
      pageNumbers.push(i);
    }

 const items = item_model(currentPosts)
    //Set current page
    const setPage = (pageNum) => {
      this.setState({currentPage: pageNum})
    }
    console.log(currentPosts)
  
  if(currentPosts > this.state.postsPerPage){
      this.setState({showPagination:true})
    }

  const searchVeh = (event) => {
      event.preventDefault()
      const reqOpt = { method: 'POST', mode:'cors', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        location:this.state.location,
        category:this.state.category,
        brand:this.state.brand,
        fuel:this.state.fuel,
        used:this.state.used,
        transmission:this.state.transmission}),};
      fetch(this.urls.get, reqOpt).then(response => response.json()).then(response => {
      console.log('s',response)
      this.setState({vehicles:response})
        
    })
    }


  if(!this.state.ready){
      return html`<div class="loader-spin"></div>`;     
    } 
    
    

  return html`${this.state.ready && html`
    <div class="card card-body blur shadow-blur mx-3 mx-md-10 mt-n7" style="padding:0 !important;">
      <div class="container">
        <form role="form" method="post" onSubmit=${searchVeh} style="display: flex;">
        <div class="row">
          <div class="col-lg-12 mx-auto py-3">
            <div class="row">
          <div class="col-lg-6">
            <h6>I WANT TO BUY</h6>
          </div>
          <div class="col-lg-6 text-end d-flex justify-content-center">
            <button type="button" onClick=${({ target }) => this.setState({used:false})} class="btn btn-outline-warning ms-lg-1 me-lg-0 me-auto mt-lg-0 mt-2">BRAND NEW</button>
            <button type="button" onClick=${({ target }) => this.setState({used:true})} class="btn btn-outline-warning  ms-lg-1 me-lg-0 me-auto mt-lg-0 mt-2">SECOND HAND</button>
          </div>
        </div>
      <div class="row">
        
          <div class="col-md-2 position-relative">
            <div class="input-group input-group-dynamic">
                    <select class="select-css" onChange=${({ target }) => this.setState({location:target.value})} name="location">
                      <option value="">Location</option>
                      <option value="nairobi">NAIROBI</option>
                      <option value="mombasa">MOMBASA</option>
                    </select>
                  </div>


                </div>

                <input type="hidden" name="make" />
                <input type="hidden" name="models" />

                <div class="col-md-2 position-relative">

                  <div class="input-group input-group-dynamic">
                    <select name="category" onChange=${({ target }) => this.setState({category:target.value})} class="select-css">
                      <option value="">All Category</option>
                      <option value="sedan">SEDAN & HATCHBACK</option>
                      <option value="suv">SUV</option>
                      <option value="pickups">PICK UPS</option>
                      <option value="buses">BUSES VANS & MPVS</option>
                    </select>
                  </div>

                </div>

                <div class="col-md-2 position-relative">

                  <div class="input-group input-group-dynamic">
                    <select name="brand" onChange=${({ target }) => this.setState({brand:target.value})}  class="select-css">
                      <option value="">All Models</option>
                      <option value="toyota">TOYOTA</option>
                      <option value="nissan">NISSAN</option>
                      <option value="mazda">MAZDA</option>
                      <option value="subaru">SUBARU</option>
                      <option value="isuzu">ISUZU</option>
                      <option value="mistubishi">MISTUBISHI</option>
                      <option value="honda">HONDA</option>
                      <option value="bmw">BMW</option>
                      <option value="benz">BENZ</option>
                      <option value="other">OTHER</option>
                    </select>
                  </div>
                </div>



                <div class="col-md-2 position-relative">

                  <div class="input-group input-group-dynamic">
                    <select class="select-css" name="fuel" onChange=${({ target }) => this.setState({fuel:target.value})} aria-label="First Name...">
                      <option value="">Fuel Type</option>
                      <option value="disel">DISEL</option>
                      <option value="electric">ELECTRIC</option>
                      <option value="petrol">PETROL</option>
                      <option value="hybrid">HYBRID</option>
                    </select>
                  </div>

                </div>


                <div class="col-md-2 position-relative">

                  <div class="input-group input-group-dynamic">
                    <select class="select-css" name="transmission" onChange=${({ target }) => this.setState({transmission:target.value})} aria-label="First Name...">
                      <option value="">Transmission</option>
                      <option value="automatic">AUTOMATIC</option>
                      <option value="manual">MANUAL</option>
                      <option value="hybrid">HYBRID</option>
                    </select>
                  </div>

                </div>


                <div class="col-md-2">

                  <div class="input-group input-group-dynamic text-end">
                    <button type="submit" class="btn bg-gradient-warning">
                      <span class="btn-inner--icon"><i class="fa fa-search"></i></span>
                      <span class="btn-inner--text">Search</span>
                    </button>
                  </div>


                </div>

              </form>
            </div>
          </div>
        </div>
      </div>
          </div>` }
      ${this.state.ready && html`<div class="container">
      <div class="row pt-3 pb-4">

        <div class="col-lg-8 mx-auto">
          <h3>New Arrivals</h3>
        </div>
        <div class="col-lg-4 mx-auto">
          <div class="nav-wrapper position-relative end-0">


            <ul class="nav nav-pills nav-fill p-1" id="pills-tab" role="tablist">

              <li class="nav-item" role="presentation">
                <a class="nav-link mb-0 px-0 py-1" type="button">
                  (${this.state.vehicles.length}) Vehicle(s) Found
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>` }

  ${items.map((item) => html`
    <div class="col-md-3 mt-4">

            <a href="/vehicle/${item.id}">
              
    <div class="card shadow-lg mt-4">

          <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
            <a class="d-block blur-shadow-image">
              <img src=${item.image_url} style="width:100%"/>
            </a>
          </div>

          <div class="card-body">
            <h6>${item.name}</h6>
          </div>

        </div>
        </a>
      </div>

            `)}`

  }
}

render(html`<${App} />`, document.getElementById('body-vehicles'));
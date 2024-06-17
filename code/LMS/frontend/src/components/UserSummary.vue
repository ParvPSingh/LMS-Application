<template>
    <div>
    <NavBar></NavBar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <br>
    <h3>User <small class="text-body-secondary">Summary</small></h3><br>
    <h4>Book <small class="text-body-secondary">Deadlines</small></h4>
    <div class="card center" style="width: 35rem;">
    <ul class="list-group list-group-flush" v-for="req in req_deadline" :key="req.req_id">
        <li class="list-group-item"><h5>{{ req.book_name }} > {{ req.book_deadline }}</h5></li>
    </ul>
    </div>
    <br><br>
    <h4>Number of Books <small class="text-body-secondary">issued</small></h4> {{ this.no_of_books }}
    <br><br>
    <h4>Number of Requests <small class="text-body-secondary">made</small></h4> {{ this.no_of_requests }}
    <br><br>
    <h4>Distribution of <small class="text-body-secondary">All Books Availability</small></h4>
    <img :src="imageSource1" alt="graph">
    <br>
    <h4>Distribution of <small class="text-body-secondary">Users's Active Requests</small></h4>
    <img :src="imageSource2" alt="graph">
    <br>
    <h4>Distribution of <small class="text-body-secondary">User's Book Authors</small></h4>
    <img :src="imageSource3" alt="graph">
    <br>
    <h4>Distribution of <small class="text-body-secondary">Usr's Book Genres</small></h4>
    <img :src="imageSource4" alt="graph">
    <br>



</template>
<script>

import axios from 'axios'
import NavBar from './NavBar.vue'
    export default{
        name: "UserSummary",
        data() {
            return {
            my_summary: [],
            no_of_books:null,
            no_of_requests:null,
            req_deadline:[],
            token: null,
            error: null,
            user_id: null,
            error_message: null,
            image1: '',
            image2: '',
            image3: '',
            image4: '',

            }
        },
        created(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.user_id = JSON.parse(user).user_id
            }
            this.image1 = 'graph_'+this.user_id+'_book_availability_dist.png';
            this.image2 = 'graph_'+this.user_id+'_active_requests.png',
            this.image3 = 'graph_'+this.user_id+'_book_authors_dist.png',
            this.image4 = 'graph_'+this.user_id+'_book_genres_dist.png'
        },
        computed: {
            imageSource1() {
                return require('@/assets/' + this.image1);
            },
            imageSource2() {
                return require('@/assets/' + this.image2);
            },
            imageSource3() {
                return require('@/assets/' + this.image3);
            },
            imageSource4() {
                return require('@/assets/' + this.image4);
            }
        },
        components:{
            NavBar
        },
        methods:{
            async return_book(book_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/return_book/${book_id}`, {}, {
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if(response.status==200){
                    this.$router.go();
                }
        }
            catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                console.error("Error:", error);
            }
        },
    },
        async mounted(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
                this.user_id = JSON.parse(user).user_id
            }
            console.log(user)
            if(user==null){
                this.$router.push({name:'SignUp'})
            }
            if (user) {
                let role = JSON.parse(user).role
                console.log(role)
                if (role == "librarian") {
                    this.$router.push({ name: 'LibrarianDashboard' })
                }
            }
            try {
                const response = await axios.get(`http://127.0.0.1:5000/summary/${this.user_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.my_summary = response.data;
                    this.no_of_books = this.my_summary[0];
                    this.no_of_requests = this.my_summary[1];
                    this.req_deadline = this.my_summary[2];
                    console.log(this.my_summary)
                } else {
                    throw new Error(response.status);
                }
                } catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
            
        }
    };
</script>
<style>
.error-message {
    background-color: #f44330;
    color: #fff;
    padding: 10px;
    margin: 0 auto;
    width: 50%;
    text-align: center;
    border-radius: 5px; 
    opacity: 0; 
    animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
.center {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
          }
</style>
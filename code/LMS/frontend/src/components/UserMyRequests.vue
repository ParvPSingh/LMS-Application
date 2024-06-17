<template>
    <div>
    <NavBar></NavBar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <h3>Active <small class="text-body-secondary">Requests</small></h3>
    <div class="card len" v-for="req in active_requests" :key="req.req_id">
    <h5 class="card-header">{{ req.book_name }}</h5>
    <div class="card-body">
        <h6 class="card-title">Book id: {{ req.book_id }}</h6>
    </div>
    </div>
    <h3>Inactive <small class="text-body-secondary">Requests</small></h3>
    <div class="card len opaque" v-for="req in inactive_requests" :key="req.req_id">
    <h5 class="card-header">{{ req.book_name }}</h5>
    <div class="card-body">
        <h6 class="card-title">Book id: {{ req.book_id }}</h6>
    </div>
    </div>
</template>
<script>

import axios from 'axios'
import NavBar from './NavBar.vue';
    export default{
        name: "UserMyRequests",
        data() {
            return {
            active_requests: [],
            inactive_requests: [],
            sec_id: null,
            token: null,
            error: null,
            error_message: null,
            user_id: null
            }
        },
        components:{
            NavBar
        },
        async mounted(){
            console.log(this.sec_id)
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
                this.user_id = JSON.parse(user).user_id;
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
                const response = await axios.get(`http://127.0.0.1:5000/my_requests/${this.user_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.active_requests = response.data[0];
                    this.inactive_requests = response.data[1];
                    console.log(this.active_requests)
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
.len{
    width:95%;
    margin: 30px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;    
}

.len:hover{
    transform: translateY(-5px);
}

.opaque{
    opacity: 0.6;
}
</style>
<template>
    <div>
    <LibrarianNavbar></LibrarianNavbar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <br>
    <h3>Active <small class="text-body-secondary">Requests</small></h3>
    <div class="card len" v-for="req in active_requests" :key="req.req_id">
    <h5 class="card-header">{{ req.book_name }} | {{ req.user_name }}</h5>
    <div class="card-body">
        <h6 class="card-title">Book id: {{ req.book_id }}   |   User's id: {{ req.user_id }}</h6>
        <p class="card-text">
            <button type="button" class="btn btn-success" v-on:click="accept_request(req.req_id)">Accept Request</button> <button type="button" class="btn btn-danger" v-on:click="delete_request(req.req_id)">Reject Request</button> <button type="button" class="btn btn-secondary" v-on:click="revoke_user(req.user_id)">Revoke User</button></p>
    </div>
    </div>
    <h3>Inactive <small class="text-body-secondary">Requests</small></h3>
    <div class="card len opaque" v-for="req in inactive_requests" :key="req.req_id">
    <h5 class="card-header">{{ req.book_name }} | {{ req.user_name }}</h5>
    <div class="card-body">
        <h6 class="card-title">Book id: {{ req.book_id }}   |   User's id: {{ req.user_id }}</h6>
        <p class="card-text">
            <button type="button" class="btn btn-danger" v-on:click="delete_request(req.req_id)">Delete Request</button> <button type="button" class="btn btn-secondary" v-on:click="revoke_user(req.user_id)">Revoke User</button></p>
    </div>
    </div>
</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue';
    export default{
        name: "LibrarianRequestPage",
        data() {
            return {
            active_requests: [],
            inactive_requests: [],
            sec_id: null,
            token: null,
            error: null,
            error_message: null,
            }
        },
        components:{
            LibrarianNavbar
        },
        methods:{
            async revoke_user(user_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/revoke_user/${user_id}`, {}, {
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if(response.status==200){
                    this.$router.go();
                }else {
                    throw new Error(response.status);
                }
        }
        catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
        },
            async delete_request(req_id){
                try{
                let response = await axios.delete(`http://127.0.0.1:5000/api/req/${req_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if(response.status==200){
                    this.$router.go();
                }
                else {
                    throw new Error(response.status);
                }
        }
        catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
        },
        async accept_request(req_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/accept_req/${req_id}`, {}, {
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if(response.status==200){
                    this.$router.go();
                }
                else {
                    throw new Error(response.status);
                }
        }
        catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
        }
        },
        async mounted(){
            console.log(this.sec_id)
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
            }
            console.log(user)
            if(user==null){
                this.$router.push({name:'SignUp'})
            }
            if (user) {
                let role = JSON.parse(user).role
                console.log(role)
                if (role == "user") {
                    this.$router.push({ name: 'HomePage' })
                }
            }
            try {
                const response = await axios.get(`http://127.0.0.1:5000/all_requests`,{
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
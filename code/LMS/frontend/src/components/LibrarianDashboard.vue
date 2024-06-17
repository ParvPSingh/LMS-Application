<template>
    <div>
    <LibrarianNavbar></LibrarianNavbar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <div class="form-containerr">
    <input type="email" class="form-controll" id="exampleFormControlInput1" placeholder="Find Genre" v-model="this.sec_name">
    <button type="submit" class="btn btn-primary" v-on:click="search(this.sec_name, )">Search</button>
</div>
    <br>
<div class="book-container">
    <div class="book-card" style="width: 18rem;" v-for="section in all_sections" :key="section.sec_id">
    <RouterLink class="nav-link" aria-current="page" :to="{ name: 'LibrarianSecwiseBooks', params: { sec_id: section.sec_id } }">
    <img src="https://t3.ftcdn.net/jpg/04/90/51/38/360_F_490513853_kAVSEYFTKn4FIi7mm63yIiXSVRxj10NH.jpg" class="card-img-top" alt="Section photo">
    </RouterLink>
    <div class="card-body">
        <h5 class="card-title">{{ section.sec_name }}</h5>
        <p class="card-text">{{ section.sec_description }}</p>
    </div>
    <ul class="list-group list-group-flush">
        <li class="list-group-item"><RouterLink class="nav-link" aria-current="page" :to="{ name: 'LibrarianAddBook', params: { sec_id: section.sec_id } }">
        <button type="button" class="btn btn-primary">Add Book</button></RouterLink></li>
        <li class="list-group-item"><RouterLink class="nav-link" aria-current="page" :to="{ name: 'LibrarianUpdateSection', params: { sec_id: section.sec_id } }">
        <button type="button" class="btn btn-secondary">Update Section</button></RouterLink></li>
        <li class="list-group-item"><button type="button" class="btn btn-secondary" v-on:click="delete_section(section.sec_id)">Delete Section</button></li>
    </ul>
    </div>
</div>
<div class="row">
        <div class="col-4"></div>
        <div class="col-4">
        <span class="center" id="add_list">
            <RouterLink class="nav-link" aria-current="page" to="/add_section">
            <img src="https://www.pngkit.com/png/full/670-6706313_plus-button-green.png" alt="add button" width="70" height="70">
            </RouterLink>
        </span>
        </div>
    </div>
</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue'
    export default{
        name: "LibrarianDashboard",
        data() {
            return {
            all_sections: [],
            token: null,
            error: null,
            error_message: null,
            sec_name:null
            }
        },
        components:{
            LibrarianNavbar
        },
        methods:{
            async delete_section(sec_id){
                try{
                let response = await axios.delete(`http://127.0.0.1:5000/api/sec/${sec_id}`,{
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
                }
        },
        async search(sec_name){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/all_sections_search/${sec_name}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.all_sections = response.data;
                    console.log(this.all_sections)
                } else {
                    throw new Error(response.status);
                }
                }catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
        }
        },
        async mounted(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
            }
            console.log(user)
            if(user==null){
                this.$router.push({name:'LogIn'})
            }
            if (user) {
                let role = JSON.parse(user).role
                console.log(role)
                if (role == "user") {
                    this.$router.push({ name: 'HomePage' })
                }
                if (role == "librarian") {
                    this.$router.push({ name: 'LibrarianDashboard' })
                }
            }
                try {
                const response = await axios.get("http://127.0.0.1:5000/all_sections",{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.all_sections = response.data;
                    console.log(this.all_sections)
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

.form-containerr {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    margin-top: 20px; 
}

.form-controll {
    width: 300px;
    margin-right: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    padding: 8px;
}

.section-css {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
}

.book-container-unavailable {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    opacity: 0.6;
}

.section-card-css {
    width: 300px;
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.section-card-css:hover {
    transform: translateY(-5px);
}

.book-image {
    text-align: center;
}
</style>
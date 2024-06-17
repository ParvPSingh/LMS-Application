import HomePage from './components/HomePage.vue'
import LogIn from './components/LogIn.vue'
import SignUp from './components/SignUp.vue'
import LibrarianAddSection from './components/LibrarianAddSection.vue'
import LibrarianUpdateSection from './components/LibrarianUpdateSection.vue'
import LibrarianAddBook from './components/LibrarianAddBook.vue'
import LibrarianUpdateBook from './components/LibrarianUpdateBook.vue'
import LibrarianDashboard from './components/LibrarianDashboard.vue'
import LibrarianRequestPage from './components/LibrarianRequestPage.vue'
import LibrarianSummary from './components/LibrarianSummary.vue'
import LibrarianUserInfo from './components/LibrarianUserInfo.vue'
import LibrarianSecwiseBooks from './components/LibrarianSecwiseBooks.vue'
import LibrarianFeedbackPage from './components/LibrarianFeedbackPage.vue'
import UserMyBooks from './components/UserMyBooks.vue'
import UserMyRequests from './components/UserMyRequests.vue'
import UserSummary from './components/UserSummary.vue'
import UserAddFeedback from './components/UserAddFeedback.vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes=[
    { path: '/', component: HomePage, name: 'HomePage' },
    { path: '/signup', component: SignUp, name: 'SignUp' },
    { path: '/login', component: LogIn, name: 'LogIn' },
    { path: '/add_section', component: LibrarianAddSection, name: 'LibrarianAddSection' },
    { path: '/update_section/:sec_id', component: LibrarianUpdateSection, name: 'LibrarianUpdateSection' },
    { path: '/add_book/:sec_id', component: LibrarianAddBook, name: 'LibrarianAddBook' },
    { path: '/update_book/:book_id', component: LibrarianUpdateBook, name: 'LibrarianUpdateBook' },
    { path: '/librarian_dashboard', component: LibrarianDashboard, name: 'LibrarianDashboard' },
    { path: '/librarian_request_page', component: LibrarianRequestPage, name: 'LibrarianRequestPage' },
    { path: '/librarian_summary', component: LibrarianSummary, name: 'LibrarianSummary' },
    { path: '/librarian_userinfo', component: LibrarianUserInfo, name: 'LibrarianUserInfo' },
    { path: '/librarian_secwise_books/:sec_id', component: LibrarianSecwiseBooks, name: 'LibrarianSecwiseBooks' },
    { path: '/librarian_feedback_page', component: LibrarianFeedbackPage, name: 'LibrarianFeedbackPage' },
    { path: '/my_books/:user_id', component: UserMyBooks, name: 'UserMyBooks' },
    { path: '/my_requests/:user_id', component: UserMyRequests, name: 'UserMyRequests' },
    { path: '/user_summary/:user_id', component: UserSummary, name: 'UserSummary' },
    { path: '/user_add_feedback/:book_id', component: UserAddFeedback, name: 'UserAddFeedback' },
]

const router = createRouter({
    history:createWebHistory(),
    routes: routes
})

export default router
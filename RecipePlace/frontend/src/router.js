import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue"
import Question from "./views/Question.vue";
import QuestionEditor from "./views/QuestionEditor";
import AnswerEditor from "./views/AnswerEditor";
import NotFound from "./views/NotFound";

Vue.use(Router);

export default new Router({
    mode: "history",
    routes: [
        {
            path: "/home",
            name: "home",
            component: Home
        },
        {
            path: "/home/question/:slug",
            name: "question",
            component: Question,
            props: true
        },
        {
            path: "/home/answer/:id",
            name: "answer-editor",
            component: AnswerEditor,
            props: true
        },
        {
            path: "/home/ask/:slug?",
            name: "question-editor",
            component: QuestionEditor,
            props: true
        },
       // {
       //     path: "*/media",
       //     name: "page-not-found",
       //     component: NotFound
       //  },

    ]
});
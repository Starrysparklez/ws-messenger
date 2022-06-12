var app = new Vue({
    el: '#app',
    data: {
        containerOpen: false
    },
    methods: {
        switchContainer: function () {
            this.containerOpen = !this.containerOpen;
        }
    }
})
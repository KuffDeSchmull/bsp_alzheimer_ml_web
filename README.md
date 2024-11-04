## Use

First install all the required dependencies and tools, as listed in the sections below.
Proceed to start the frontend with 
``` 
npm run dev 
```
Then start the backend server, by launching the server.py file.
Visit the page in your browser, the local URL and Port should be 

> http://127.0.0.1:5173/

## Vue.JS

> Requirements: NodeJS >=20.9.0 and npm, Vite >= v4.5.0

```
npm install -g @vue/cli

npm install
npm run format

npm run dev
```

#### Features

- VueJS router
- Pinia state management
- Vitest Unit Testing
- Cypress End-to-End Testing
- Typescript, ESLint, Prettier

> Dev Port: 5173

## Bun REST API server

> Requirements: Bun >=1.0.8 and npm and python3(iff)

While a Bun or NodeJS backend was initially planned, the careful decision has been made to instead use python for a backend. As 'screening' is already done in python, so in order to keep complexity to a minimum, we decided against an additional component.

## Python Backend

> Requirements: Python3 env with PyTorch and Flask

- Contains a requirements.txt for all the dependencies
- server.py is the entry file
- run the entry file to start the development server

#### Features

> Dev Port: 5000

## Deployment - NGINX

For deployment use as a Reverse Proxy for the Front- and Back-end, may also be used as a load-balancer.
To prepare the frontend to be used with an NGINX server, we need to build it.
```
npm run build
```
This produces static files, that we can serve with NGINX. The configuration could then look something like this.
```
server {
    listen 80;
    server_name example.com; # Replace with actual domain name, if present

    # Serve static files produced by the build step
    location / {
        root /path/to/your/vue/dist; # Adjust path to the build
        try_files $uri $uri/ /index.html;
    }

    # Reverse proxy, forwards any requests to the /api endpoint to the backend REST API
    location /api {
        proxy_pass http://localhost:FLASK_PORT; # Replace localhost with public IP and  FLASK_PORT with your Flask app's port
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

This is just an example and needs further adjustments, as we should use https for escurity reasons, for example, if accessed from a public network.


## Development - Vite

For Development purposes, a proxy to the backend has been defined in the vite.config.vue, the Flask backend disables CORS for dev as well. You may need to run Chrome with CORS disabled as follows.

```
# Windows
chrome.exe --user-data-dir="C://chrome-dev-disabled-security" --disable-web-security --disable-site-isolation-trials

# macOS
open /Applications/Google\ Chrome.app --args --user-data-dir="/var/tmp/chrome-dev-disabled-security" --disable-web-security --disable-site-isolation-trials

# Linux
google-chrome --user-data-dir="~/chrome-dev-disabled-security" --disable-web-security --disable-site-isolation-trials
```

## Cypress - E2E
Open user interface for cypress
```
npx cypress open
```

## Further Explanation about components

This mono-repo includes 2 different components, the Vue 3 bspFrontend, and the python Flask backend.

This project is also available on GitLab, under https://gitlab.com/dementia_drawing_app/vue_ml_supported_screening
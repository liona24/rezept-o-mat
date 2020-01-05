# rezept-o-mat

## Project Setup

```bash

# Fire up a environment if desired
$ docker run -it -v $(pwd):/var/rezept-o-mat -p 8080:8080 --user=node node /bin/bash

# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev

# build for production and launch server
$ yarn build
$ yarn start

# generate static project
$ yarn generate

```

By default, the recipes are fetched from a mock JSON server. The URL can be configured in [src/api.js](src/api.js)

The demo version is hosted on github pages, [here](https://liona24.github.io/rezept-o-mat/)

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

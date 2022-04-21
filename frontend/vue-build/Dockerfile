FROM node:17-alpine3.14

WORKDIR /vue

RUN apk update
RUN npm install -g npm
RUN npm install -g @vue/cli

# ENV BASE_URL=/portal-dev
CMD ["npm", "run", "serve"]
# CMD ["sleep", "infinity"]

# Use official Node.js image as base
FROM node:14-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json to work directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port (if your Vue app runs on a specific port)
EXPOSE 8080
WORKDIR /app/client

# Command to run the application
CMD ["npm", "run", "serve"]


# Use the official Cowrie image as the base image
FROM cowrie/cowrie:latest

# Set the working directory inside the container
WORKDIR /cowrie

# Copy the custom configuration files into the container (optional)
# If you have a custom cowrie.cfg, make sure to copy it into the container
# Make sure your config is located in the local `config` directory.
COPY ./config/cowrie.cfg /cowrie/etc/cowrie.cfg

# Expose the necessary ports
EXPOSE 22 2222 8080

# The entrypoint for the Cowrie honeypot service
ENTRYPOINT ["cowrie", "start"]

# Run Cowrie (if the base image doesn't define it, you can also explicitly use the command here)
CMD ["-c", "/cowrie/etc/cowrie.cfg"]

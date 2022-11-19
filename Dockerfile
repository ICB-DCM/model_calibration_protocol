FROM ubuntu:20.04
LABEL description="Model calibration protocol examples."

# Setup a user with privileges for administration.
RUN apt-get update
RUN apt-get install -y sudo
RUN adduser --disabled-password --gecos '' user
RUN adduser user sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
# Switch user.
USER user
WORKDIR /home/user

# Install dependencies.
RUN sudo apt-get update
# Install Python dependencies.
RUN sudo apt-get install -y python3 python3-pip
# Install AMICI dependencies
RUN sudo apt-get install -y libatlas-base-dev swig libhdf5-serial-dev

# Clone the tutorial git repository.
RUN sudo apt-get install -y git
RUN git clone --recurse-submodules https://github.com/ICB-DCM/model_calibration_protocol
# Setup the Python environment.
RUN echo 'export PATH=/home/user/.local/bin:$PATH' >> /home/user/.bashrc
ENV PATH="/home/user/.local/bin:$PATH"
RUN pip3 install pip==22.3.1 setuptools==65.5.1 wheel==0.38.4
RUN pip3 install -r model_calibration_protocol/requirements.txt

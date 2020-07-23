#FROM continuumio/miniconda

#ENV BK_VERSION=1.4.0
#ENV PY_VERSION=3.7
#ENV NUM_PROCS=4
#ENV BOKEH_RESOURCES=cdn

#RUN apt-get install git bash

#RUN git clone https://github.com/elrufaie/capstone-presidential-election.git
#RUN cd capstone-presidential-election/
#RUN conda install --yes --quiet python=${PY_VERSION} pyyaml jinja2 bokeh=${BK_VERSION} numpy #"nodejs>=8.8" pandas geopandas flask requests scikit-learn matplotlib lxml
#RUN conda install -c anaconda lxml
#RUN conda clean -ay

#EXPOSE 8080

#RUN python -c "import bokeh.sampledata; bokeh.sampledata.download()"
#RUN cd capstone-presidential-election
#CMD python main.py
#CMD bokeh serve --port 8080 sample-bokeh-app

FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt 
EXPOSE 8080
CMD python3 main.py 
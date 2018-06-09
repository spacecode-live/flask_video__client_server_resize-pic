# flask_video__client_server_resize-pic

A service that can resize images-
Independent software client processes able to ‘connect’
to the service in some way. These clients may be local (on the same machine), 
or (for extra points), the service could allow connections from a mixture of both local and remote clients.
Note that the service should process images (single video frames), not complete videos. 
The service scaled so that many clients can use it concurrently. 
It  possible for multiple requests to be processed concurrently and all computational resources available should be utilised.
To test your service you should create a test program that uses your service to concurrently
resize N instances of a video, where N is passed as a command line argument to the test application. 
Note we are using N instances of the same video for simplicity, in reality it would be N different videos.
The scaling of each video instance should start M seconds after the previous. For example, if N = 2 and M = 10,
you test should start using your service to process one instance of the video immediately, and 10 seconds later
it should start using your service to process the second instance.  The values of N and M will be passed as command 
line parameters, as will the video path. Spliting the video into frames and make multiple calls to your service. The
test program  create N sets of output frames, saved to disk as images, e.g.  
/tmp/vid-instance1/Frame00001.jpg 
/tmp/vid-instance1/Frame00002.jpg 
/tmp/vid-instance1/Frame00003.jpg 
/tmp/vid-instance2/Frame00001.jpg 
/tmp/vid-instance2/Frame00002.jpg 
/tmp/vid-instance2/Frame00003.jpg  
… and so on.
re-sized images to disk as soon as they have been processed 
(as opposed to converting all frames and then writing them to disk at the end). 
Make your test report runtime metrics including the frame-rate of the conversion
(a running average) for each video instance, reported when each video instance has
been completely converted,  display-  total amount of time taken for each instance. 

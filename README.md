# cinder-csi
GRPC Server implementation of CSI spec for Cinder

This repo is an experimentation repo to try some different
things with CSI and Cinder.  The main idea here being to see
if it's feasible to omit the shim layer and usage of Gophercloud
(don't get me wrong, Gophercloud is awesome), but the idea here
is that it *should* be possible to just drop in a replacement for
Cinder's current REST API service (ie just run a GRPC server that
implements the CSI spec).

We just use the standard grpc generation tools, just like we do
with any CSI driver, but we generate the output files in Python
instead of Golang.

As a result, we can just drop this server into a Cinder deployment
and provide its endpoint to our CSI client and get CSI natively (ish)
in Cinder.

## There are two very basic examples in this repo

### Using a full blown Cinder and creating a client session

The server file to do this is ```csi_server.py```

### Using bypassing the Cinder API services accessing Cinder Python directly

The server file to do this is ```direct_server.py```


NOTE
All of this is offensively INCOMPLETE right now, this is just
place to try some things out, and provide examples of ideas.


## Test it out
Not much here, but we can test basic connection to a csi client and
the ability to send requests directly out to a running cinder install.

I used the rexray csc tool for this, here's the basic outline to try
things out:

Update the cloud variables in the csi_server.py file to have the right
endpoint and credential info for you, then just run the server:

```python ./csi_server.py
```

or

```
  python ./direct_server.py
```

You should be greeted with a "now serving..." message when it's ready.
Note that we serve up on prot 50051 for now.

Next grab the rexray csc (may be out of date, but good enough for a starting
point):  https://github.com/rexray/gocsi/tree/master/csc

Make and install the csc tool, then you can start messing around with things:

```csc controller create-volume --cap 5,1 \
        --log-level=debug \
        -e tcp://10.117.33.4:50051 \
        muahuahhuah
```

Note the example above is specifying use of a tcp socket and the IP specified
is the IP of the node running the csi_server.

You can also delete the volumes you created by UUID or Name:

```csc controller delete-volume \
        --log-level=debug \
        -e tcp://10.117.33.4:50051 \
        9813254f-d46e-4683-aa0d-998f9dc5fa0c
```

List is broken(well lots of things are missing or broken), but hey... PR's are WELCOME :)



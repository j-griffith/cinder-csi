# cinder-csi
Direct grpc implementation of CSI spec for Cinder

NOTE this doesn't work right now, it's very much incomplete and
has a lot of work to be done if it seems worthwhile.

In the spirit of "baby-steps" or "iterative development", we're
going to avoid all the ugliness of trying to import and serialize
all of Cinder Object structure and other crap that is problematic
for now.  Instead we'll just start with the simple case of using
an external cinder and use the client.  This can be modified for
stand-alone (ie no keystone) pretty easily, but for now just see
if this idea is even feasible.

The advantage of this approach is that there's no need for glue
or shim code between a CSI driver and Cinder (ie don't need to
duplicate every call using Gophercloud).  Instead, this interface
would just import and call cinder.volume.api directly.
(NOTE just importing cinder.volume is tricky, may or may not be
worth it, so for now use a client with full blown cinder api 
service.

There's certainly a bit of extra features that are missed by doing
this, but currently in the context of a standalone Cinder and CSI 
I'm not sure we're missing anything.

This also provides a pattern for creating shims/plugins for other
things as well.  One thing that's been mentioned is Swordfish, but
this model could extend to other things like an EBS compat layer
etc.  

## Test it out
Not much here, but we can test basic connection to a csi client and 
the ability to send requests directly out to a running cinder install.

I used the rexray csc tool for this, here's the basic outline to try
things out:

Update the cloud variables in the csi_server.py file to have the right
endpoint and credential info for you, then just run the server:

```python ./csi_server.py
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

List is broken, but hey... PR's are WELCOME :)



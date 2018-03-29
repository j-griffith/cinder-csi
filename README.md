# cinder-csi
Direct grpc implementation of CSI spec for Cinder

NOTE this doesn't work right now, it's very much incomplete and
has a lot of work to be done if it seems worthwhile.

The advantage of this approach is that there's no need for glue
or shim code between a CSI driver and Cinder (ie don't need to
duplicate every call using Gophercloud).  Instead, this interface
would just import and call cinder.volume.api directly.

There's certainly a bit of extra features that are missed by doing
this, but currently in the context of a standalone Cinder and CSI 
I'm not sure we're missing anything.

This also provides a pattern for creating shims/plugins for other
things as well.  One thing that's been mentioned is Swordfish, but
this model could extend to other things like an EBS compat layer
etc.  

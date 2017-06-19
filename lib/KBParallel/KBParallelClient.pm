package KBParallel::KBParallelClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
use Time::HiRes;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

KBParallel::KBParallelClient

=head1 DESCRIPTION


A KBase module: KBParallel


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => KBParallel::KBParallelClient::RpcClient->new,
	url => $url,
	headers => [],
    };
    my %arg_hash = @args;
    $self->{async_job_check_time} = 0.1;
    if (exists $arg_hash{"async_job_check_time_ms"}) {
        $self->{async_job_check_time} = $arg_hash{"async_job_check_time_ms"} / 1000.0;
    }
    $self->{async_job_check_time_scale_percent} = 150;
    if (exists $arg_hash{"async_job_check_time_scale_percent"}) {
        $self->{async_job_check_time_scale_percent} = $arg_hash{"async_job_check_time_scale_percent"};
    }
    $self->{async_job_check_max_time} = 300;  # 5 minutes
    if (exists $arg_hash{"async_job_check_max_time_ms"}) {
        $self->{async_job_check_max_time} = $arg_hash{"async_job_check_max_time_ms"} / 1000.0;
    }
    my $service_version = undef;
    if (exists $arg_hash{"service_version"}) {
        $service_version = $arg_hash{"service_version"};
    }
    $self->{service_version} = $service_version;

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}

sub _check_job {
    my($self, @args) = @_;
# Authentication: ${method.authentication}
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function _check_job (received $n, expecting 1)");
    }
    {
        my($job_id) = @args;
        my @_bad_arguments;
        (!ref($job_id)) or push(@_bad_arguments, "Invalid type for argument 0 \"job_id\" (it should be a string)");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to _check_job:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => '_check_job');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "KBParallel._check_job",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => '_check_job',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method _check_job",
                        status_line => $self->{client}->status_line,
                        method_name => '_check_job');
    }
}




=head2 run_batch

  $results = $obj->run_batch($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a KBParallel.RunBatchParams
$results is a KBParallel.BatchResults
RunBatchParams is a reference to a hash where the following keys are defined:
	tasks has a value which is a reference to a list where each element is a KBParallel.Task
	concurrent_local_tasks has a value which is an int
	concurrent_njsw_tasks has a value which is an int
	n_retry_failed_tasks has a value which is an int
Task is a reference to a hash where the following keys are defined:
	function has a value which is a KBParallel.Function
	params has a value which is an UnspecifiedObject, which can hold any non-null object
	run_local has a value which is a KBParallel.boolean
Function is a reference to a hash where the following keys are defined:
	name has a value which is a string
	module_name has a value which is a string
	version has a value which is a string
boolean is an int
BatchResults is a reference to a hash where the following keys are defined:
	results has a value which is a reference to a list where each element is a KBParallel.TaskResult
TaskResult is a reference to a hash where the following keys are defined:
	function has a value which is a KBParallel.Function
	params has a value which is an UnspecifiedObject, which can hold any non-null object
	returned has a value which is an UnspecifiedObject, which can hold any non-null object
	error has a value which is an UnspecifiedObject, which can hold any non-null object
	run_context has a value which is a KBParallel.RunContext
RunContext is a reference to a hash where the following keys are defined:
	location has a value which is a string
	job_id has a value which is a string

</pre>

=end html

=begin text

$params is a KBParallel.RunBatchParams
$results is a KBParallel.BatchResults
RunBatchParams is a reference to a hash where the following keys are defined:
	tasks has a value which is a reference to a list where each element is a KBParallel.Task
	concurrent_local_tasks has a value which is an int
	concurrent_njsw_tasks has a value which is an int
	n_retry_failed_tasks has a value which is an int
Task is a reference to a hash where the following keys are defined:
	function has a value which is a KBParallel.Function
	params has a value which is an UnspecifiedObject, which can hold any non-null object
	run_local has a value which is a KBParallel.boolean
Function is a reference to a hash where the following keys are defined:
	name has a value which is a string
	module_name has a value which is a string
	version has a value which is a string
boolean is an int
BatchResults is a reference to a hash where the following keys are defined:
	results has a value which is a reference to a list where each element is a KBParallel.TaskResult
TaskResult is a reference to a hash where the following keys are defined:
	function has a value which is a KBParallel.Function
	params has a value which is an UnspecifiedObject, which can hold any non-null object
	returned has a value which is an UnspecifiedObject, which can hold any non-null object
	error has a value which is an UnspecifiedObject, which can hold any non-null object
	run_context has a value which is a KBParallel.RunContext
RunContext is a reference to a hash where the following keys are defined:
	location has a value which is a string
	job_id has a value which is a string


=end text

=item Description



=back

=cut

 sub run_batch
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function run_batch (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to run_batch:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'run_batch');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "KBParallel.run_batch",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'run_batch',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method run_batch",
					    status_line => $self->{client}->status_line,
					    method_name => 'run_batch',
				       );
    }
}
 


=head2 run

  $return = $obj->run($input_params)

=over 4

=item Parameter and return types

=begin html

<pre>
$input_params is a KBParallel.KBParallelrunInputParams
$return is an UnspecifiedObject, which can hold any non-null object
KBParallelrunInputParams is a reference to a hash where the following keys are defined:
	method has a value which is a KBParallel.FullMethodQualifier
	prepare_method has a value which is a KBParallel.FullMethodQualifier
	is_local has a value which is a KBParallel.boolean
	global_input has a value which is an UnspecifiedObject, which can hold any non-null object
	time_limit has a value which is an int
FullMethodQualifier is a reference to a hash where the following keys are defined:
	module_name has a value which is a string
	method_name has a value which is a string
	service_ver has a value which is a string
boolean is an int

</pre>

=end html

=begin text

$input_params is a KBParallel.KBParallelrunInputParams
$return is an UnspecifiedObject, which can hold any non-null object
KBParallelrunInputParams is a reference to a hash where the following keys are defined:
	method has a value which is a KBParallel.FullMethodQualifier
	prepare_method has a value which is a KBParallel.FullMethodQualifier
	is_local has a value which is a KBParallel.boolean
	global_input has a value which is an UnspecifiedObject, which can hold any non-null object
	time_limit has a value which is an int
FullMethodQualifier is a reference to a hash where the following keys are defined:
	module_name has a value which is a string
	method_name has a value which is a string
	service_ver has a value which is a string
boolean is an int


=end text

=item Description



=back

=cut

sub run
{
    my($self, @args) = @_;
    my $job_id = $self->_run_submit(@args);
    my $async_job_check_time = $self->{async_job_check_time};
    while (1) {
        Time::HiRes::sleep($async_job_check_time);
        $async_job_check_time *= $self->{async_job_check_time_scale_percent} / 100.0;
        if ($async_job_check_time > $self->{async_job_check_max_time}) {
            $async_job_check_time = $self->{async_job_check_max_time};
        }
        my $job_state_ref = $self->_check_job($job_id);
        if ($job_state_ref->{"finished"} != 0) {
            if (!exists $job_state_ref->{"result"}) {
                $job_state_ref->{"result"} = [];
            }
            return wantarray ? @{$job_state_ref->{"result"}} : $job_state_ref->{"result"}->[0];
        }
    }
}

sub _run_submit {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function _run_submit (received $n, expecting 1)");
    }
    {
        my($input_params) = @args;
        my @_bad_arguments;
        (ref($input_params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"input_params\" (value was \"$input_params\")");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to _run_submit:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => '_run_submit');
        }
    }
    my $context = undef;
    if ($self->{service_version}) {
        $context = {'service_ver' => $self->{service_version}};
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "KBParallel._run_submit",
        params => \@args, context => $context});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => '_run_submit',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
            );
        } else {
            return $result->result->[0];  # job_id
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method _run_submit",
                        status_line => $self->{client}->status_line,
                        method_name => '_run_submit');
    }
}

 


=head2 job_status

  $ret = $obj->job_status($input_params)

=over 4

=item Parameter and return types

=begin html

<pre>
$input_params is a KBParallel.KBParallelstatusInputParams
$ret is a KBParallel.KBParallelstatusOutputObj
KBParallelstatusInputParams is a reference to a hash where the following keys are defined:
	joblist has a value which is a reference to a list where each element is a string
KBParallelstatusOutputObj is a reference to a hash where the following keys are defined:
	num_jobs_checked has a value which is an int
	jobstatus has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

$input_params is a KBParallel.KBParallelstatusInputParams
$ret is a KBParallel.KBParallelstatusOutputObj
KBParallelstatusInputParams is a reference to a hash where the following keys are defined:
	joblist has a value which is a reference to a list where each element is a string
KBParallelstatusOutputObj is a reference to a hash where the following keys are defined:
	num_jobs_checked has a value which is an int
	jobstatus has a value which is a reference to a list where each element is a string


=end text

=item Description



=back

=cut

 sub job_status
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function job_status (received $n, expecting 1)");
    }
    {
	my($input_params) = @args;

	my @_bad_arguments;
        (ref($input_params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"input_params\" (value was \"$input_params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to job_status:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'job_status');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "KBParallel.job_status",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'job_status',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method job_status",
					    status_line => $self->{client}->status_line,
					    method_name => 'job_status',
				       );
    }
}
 


=head2 cancel_run

  $ret = $obj->cancel_run($input_params)

=over 4

=item Parameter and return types

=begin html

<pre>
$input_params is a KBParallel.KBParallelcancel_runInput
$ret is a KBParallel.KBParallelcancel_runOutput
KBParallelcancel_runInput is a reference to a hash where the following keys are defined
KBParallelcancel_runOutput is a reference to a hash where the following keys are defined

</pre>

=end html

=begin text

$input_params is a KBParallel.KBParallelcancel_runInput
$ret is a KBParallel.KBParallelcancel_runOutput
KBParallelcancel_runInput is a reference to a hash where the following keys are defined
KBParallelcancel_runOutput is a reference to a hash where the following keys are defined


=end text

=item Description



=back

=cut

 sub cancel_run
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function cancel_run (received $n, expecting 1)");
    }
    {
	my($input_params) = @args;

	my @_bad_arguments;
        (ref($input_params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"input_params\" (value was \"$input_params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to cancel_run:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'cancel_run');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "KBParallel.cancel_run",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'cancel_run',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method cancel_run",
					    status_line => $self->{client}->status_line,
					    method_name => 'cancel_run',
				       );
    }
}
 


=head2 getlog

  $ret = $obj->getlog($input_params)

=over 4

=item Parameter and return types

=begin html

<pre>
$input_params is a KBParallel.KBParallelgetlogInput
$ret is a KBParallel.KBParallelgetlogOutput
KBParallelgetlogInput is a reference to a hash where the following keys are defined
KBParallelgetlogOutput is a reference to a hash where the following keys are defined

</pre>

=end html

=begin text

$input_params is a KBParallel.KBParallelgetlogInput
$ret is a KBParallel.KBParallelgetlogOutput
KBParallelgetlogInput is a reference to a hash where the following keys are defined
KBParallelgetlogOutput is a reference to a hash where the following keys are defined


=end text

=item Description



=back

=cut

 sub getlog
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function getlog (received $n, expecting 1)");
    }
    {
	my($input_params) = @args;

	my @_bad_arguments;
        (ref($input_params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"input_params\" (value was \"$input_params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to getlog:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'getlog');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "KBParallel.getlog",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'getlog',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method getlog",
					    status_line => $self->{client}->status_line,
					    method_name => 'getlog',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "KBParallel.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "KBParallel.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'getlog',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method getlog",
            status_line => $self->{client}->status_line,
            method_name => 'getlog',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for KBParallel::KBParallelClient\n";
    }
    if ($sMajor == 0) {
        warn "KBParallel::KBParallelClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

A boolean - 0 for false, 1 for true.
@range (0, 1)


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 Function

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
name has a value which is a string
module_name has a value which is a string
version has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
name has a value which is a string
module_name has a value which is a string
version has a value which is a string


=end text

=back



=head2 Task

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
function has a value which is a KBParallel.Function
params has a value which is an UnspecifiedObject, which can hold any non-null object
run_local has a value which is a KBParallel.boolean

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
function has a value which is a KBParallel.Function
params has a value which is an UnspecifiedObject, which can hold any non-null object
run_local has a value which is a KBParallel.boolean


=end text

=back



=head2 RunContext

=over 4



=item Description

location = local | njsw
job_id = '' | [njsw_job_id]

May want to add: AWE node ID, client group, total run time, etc


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
location has a value which is a string
job_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
location has a value which is a string
job_id has a value which is a string


=end text

=back



=head2 TaskResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
function has a value which is a KBParallel.Function
params has a value which is an UnspecifiedObject, which can hold any non-null object
returned has a value which is an UnspecifiedObject, which can hold any non-null object
error has a value which is an UnspecifiedObject, which can hold any non-null object
run_context has a value which is a KBParallel.RunContext

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
function has a value which is a KBParallel.Function
params has a value which is an UnspecifiedObject, which can hold any non-null object
returned has a value which is an UnspecifiedObject, which can hold any non-null object
error has a value which is an UnspecifiedObject, which can hold any non-null object
run_context has a value which is a KBParallel.RunContext


=end text

=back



=head2 BatchResults

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
results has a value which is a reference to a list where each element is a KBParallel.TaskResult

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
results has a value which is a reference to a list where each element is a KBParallel.TaskResult


=end text

=back



=head2 RunBatchParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
tasks has a value which is a reference to a list where each element is a KBParallel.Task
concurrent_local_tasks has a value which is an int
concurrent_njsw_tasks has a value which is an int
n_retry_failed_tasks has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
tasks has a value which is a reference to a list where each element is a KBParallel.Task
concurrent_local_tasks has a value which is an int
concurrent_njsw_tasks has a value which is an int
n_retry_failed_tasks has a value which is an int


=end text

=back



=head2 FullMethodQualifier

=over 4



=item Description

module_name - SDK module name (ie. ManyHellos, RNAseq),
method_name - method in SDK module (TopHatcall, Hiseqcall etc each will have own _prepare(),
    _runEach(), _collect() methods defined),
service_ver - optional version of SDK module (may be dev/beta/release, or symantic version
    or particular git commit hash), it's release by default,


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
module_name has a value which is a string
method_name has a value which is a string
service_ver has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
module_name has a value which is a string
method_name has a value which is a string
service_ver has a value which is a string


=end text

=back



=head2 KBParallelrunInputParams

=over 4



=item Description

Input parameters for run() method.

method - optional method where _prepare(), _runEach() and _collect() suffixes are applied,
prepare_method - optional method (if defined overrides _prepare suffix rule),
is_local - optional flag defining way of scheduling sub-job, in case is_local=false sub-jobs
    are scheduled against remote execution engine, if is_local=true then sub_jobs are run as
    local functions through CALLBACK mechanism, default value is false,
global_input - input data which is supposed to be sent as a part to 
    <module_name>.<method_name>_prepare() method,
time_limit - time limit in seconds, equals to 5000 by default.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
method has a value which is a KBParallel.FullMethodQualifier
prepare_method has a value which is a KBParallel.FullMethodQualifier
is_local has a value which is a KBParallel.boolean
global_input has a value which is an UnspecifiedObject, which can hold any non-null object
time_limit has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
method has a value which is a KBParallel.FullMethodQualifier
prepare_method has a value which is a KBParallel.FullMethodQualifier
is_local has a value which is a KBParallel.boolean
global_input has a value which is an UnspecifiedObject, which can hold any non-null object
time_limit has a value which is an int


=end text

=back



=head2 KBParallelstatusInputParams

=over 4



=item Description

status() method


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
joblist has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
joblist has a value which is a reference to a list where each element is a string


=end text

=back



=head2 KBParallelstatusOutputObj

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
num_jobs_checked has a value which is an int
jobstatus has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
num_jobs_checked has a value which is an int
jobstatus has a value which is a reference to a list where each element is a string


=end text

=back



=head2 KBParallelcancel_runInput

=over 4



=item Description

cancel_run() method


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined
</pre>

=end html

=begin text

a reference to a hash where the following keys are defined

=end text

=back



=head2 KBParallelcancel_runOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined
</pre>

=end html

=begin text

a reference to a hash where the following keys are defined

=end text

=back



=head2 KBParallelgetlogInput

=over 4



=item Description

getlog() method


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined
</pre>

=end html

=begin text

a reference to a hash where the following keys are defined

=end text

=back



=head2 KBParallelgetlogOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined
</pre>

=end html

=begin text

a reference to a hash where the following keys are defined

=end text

=back



=cut

package KBParallel::KBParallelClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;

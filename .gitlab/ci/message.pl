#! /usr/bin/env perl

## no critic (InputOutput::RequireCheckedSyscalls)

use strict;
use warnings;

use Cwd qw(cwd);
use JSON;
use LWP::UserAgent;

if (
     !$ENV{CI_COMMIT_REF_NAME}
  || !$ENV{CI_PROJECT_ID}
  || !$ENV{CI_PROJECT_NAME}
  || !$ENV{GITLAB_API_TOKEN}
  || !$ENV{MATTERMOST_API_TOKEN}
  || !$ENV{MATTERMOST_CHANNELS}
) {
  print 'Missing prerequisite';
  exit 1;
}

my $lwp = LWP::UserAgent->new;
my $gitlab = sprintf 'https://git.priv.iliad78.net/api/v4/projects/%s/repository/tags?search=%s', (
  $ENV{CI_PROJECT_ID},
  $ENV{CI_COMMIT_REF_NAME},
);
my $mattermost_file = 'https://slack.iliad78.net/api/v4/files';
my $mattermost_post = 'https://slack.iliad78.net/api/v4/posts';
my %header_gitlab = (
  Authorization => 'Bearer ' . $ENV{GITLAB_API_TOKEN},
);
my %header_mattermost = (
  Authorization => 'Bearer ' . $ENV{MATTERMOST_API_TOKEN},
);


# Message creation

my $tags = decode_json $lwp->get($gitlab, %header_gitlab)->decoded_content;
my $tag = $tags->[0];

my $fields = [];

if ($tag->{release}->{description}) {
  my $index = 0;
  my $field = {
    title => 'Changes',
    value => $tag->{release}->{description},
  };
  my @parts = split m/#+\s([^\n]+)/sm, $tag->{release}->{description};

  if (scalar @parts == 1) {
    push @{$fields}, $field;
  } else {
    for my $part (@parts) {
      $part =~ s/^\s+|\s+$//gsm;

      next unless $part;

      if ($index % 2 == 0) {
        $field->{title} = $part;
      } else {
        $field->{value} = $part;

        push @{$fields}, $field;

        $field = {};
      }

      $index++;
    }
  }
}

my $message = {
  author_icon => 'https://research.unimelb.edu.au/__data/assets/image/0003/2564283/python-logo.png',
  author_name => $ENV{CI_PROJECT_NAME},
  fallback => 'New version of ' . $ENV{CI_PROJECT_NAME} . ' available: ' . $ENV{CI_COMMIT_REF_NAME},
  fields => $fields,
  title => 'New version of ' . $ENV{CI_PROJECT_NAME} . ' available: ' . $ENV{CI_COMMIT_REF_NAME},
};


# Prepare sending

my $path = cwd() . '/dist/iliad-payment-' . substr($ENV{CI_COMMIT_REF_NAME}, 1) . '.tar.gz';

my @channels = split qr/,/sm, $ENV{MATTERMOST_CHANNELS};

print scalar @channels, " channels to inform\n";

for my $channel (@channels) {

  # File upload
  my %form = (
    Content_Type => 'form-data',
    Content => [
      channel_id => $channel,
    ],
  );

  my $files = decode_json $lwp->post($mattermost_file, %form, %header_mattermost)->decoded_content;

  if (!$files->{file_infos}) {
    print 'Message failed for channel #' . $channel . "\n";
    next;
  }

  my $file_id = $files->{file_infos}->[0]->{id};

  # Post
  my %post = (
    Content => encode_json {
      channel_id => $channel,
      file_ids => [$file_id],
      props => {
        attachments => [
          $message,
        ],
      },
    },
  );

  my $response = decode_json $lwp->post($mattermost_post, %post, %header_mattermost)->decoded_content;

  # Inform
  if ($response->{create_at}) {
    print 'Message posted';
  } else {
    print 'Message failed for channel #' . $channel;
  }

  print "\n";
}

exit 0;

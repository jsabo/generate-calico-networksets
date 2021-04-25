# calicofun

## Reference

[Aws IP Ranges by Service](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html)

[Aws Service Endpoints by Name](https://aws.amazon.com/blogs/aws/new-query-for-aws-regions-endpoints-and-more-using-aws-systems-manager-parameter-store/)

[Azure IP Ranges by Service Tag](https://www.microsoft.com/en-us/download/details.aspx?id=56519)

## Use

To use, first set the output in the *config.txt* file under the *Output Path* section.
Here the cloud provider global network sets shall be written to files with the naming convention
*<cloud_provider>GlobalNetworkSet.yaml*
Once the output path has been chosen run
> python -m global_sets_generator.main

from the root directory.
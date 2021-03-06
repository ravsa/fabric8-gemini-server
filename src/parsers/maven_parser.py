"""Maven Parser."""

from parsers.parser_base import Parser


class MavenParser(Parser):
    """Parser to parse maven co-ordinates and return package list."""

    @staticmethod
    def parse_output_file(content):
        """Parse the output file generated by mvn dependency:resolve command."""
        content_list = content.split()
        dependencies = set()
        for content in content_list:
            try:
                gav = MavenParser._parse_string(content)
                dependencies.add("{ecosystem}:{group_id}:{artifact_id}:{version}".format(
                    ecosystem="maven",
                    group_id=gav.get('groupId', ''),
                    artifact_id=gav.get('artifactId', ''),
                    version=gav.get('version', '')
                ))
            except ValueError:
                pass

        return dependencies

    @staticmethod
    def _parse_string(coordinates_str):
        """Parse string representation into a dictionary."""
        a = {'groupId': '',
             'artifactId': '',
             'packaging': '',
             'version': '',
             'classifier': ''}

        ncolons = coordinates_str.count(':')
        if ncolons == 1:
            a['groupId'], a['artifactId'] = coordinates_str.split(':')
        elif ncolons == 2:
            a['groupId'], a['artifactId'], a['version'] = coordinates_str.split(':')
        elif ncolons == 3:
            a['groupId'], a['artifactId'], a['packaging'], a['version'] = coordinates_str.split(':')
        elif ncolons == 4:
            # Usually, it's groupId:artifactId:packaging:classifier:version but here it's
            # groupId:artifactId:packaging:version:classifier
            a['groupId'], a['artifactId'], a['packaging'], a['version'], a['classifier'] = \
                coordinates_str.split(':')
        else:
            raise ValueError('Invalid Maven coordinates %s', coordinates_str)

        return a

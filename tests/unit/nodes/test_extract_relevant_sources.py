from codius.graph.nodes.extract_relevant_sources import extract_relevant_sources


def test_extract_relevant_sources_reads_expected_files(tmp_path):
    file = tmp_path / "Test.cs"
    file.write_text("// test content")

    state = {
        "intent": [{"building_block_type": "AGGREGATE_ROOT", "target": "Order"}],
        "building_blocks": [{
            "type": "AGGREGATE_ROOT",
            "name": "Order",
            "file_path": str(file),
            "namespace": "MyApp.Domain.Order"
        }],
        "project_metadata": {}
    }

    result = extract_relevant_sources(state)
    assert str(file) in result["sources"]
    assert "// test content" in result["sources"][str(file)]

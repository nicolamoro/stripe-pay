from utils.hash import generate_hash


def test_generate_hash():
    # arrange
    plaintext = "test"
    expected_result = "67cab75fdeab2d72bd8ddacdd5480a1cd03776458fa292ac874dd3b12343fc18"

    # act
    result = generate_hash(plaintext)

    # assert
    assert result == expected_result

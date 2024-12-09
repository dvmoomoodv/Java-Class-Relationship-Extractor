````markdown
# Java Class Relationship Extractor

이 스크립트는 지정한 자바 소스 디렉토리 내의 `.java` 파일들을 파싱하여 클래스 관계(상속, 구현, import)를 분석한 뒤, YAML 형태로 출력하는 유틸리티입니다.

## 기능

- 지정한 디렉토리 하위에 있는 모든 `.java` 파일을 재귀적으로 탐색합니다.
- 각 자바 파일을 파싱하여 다음과 같은 관계 정보를 추출합니다:
  - 클래스(또는 인터페이스) 이름
  - 상속(extends) 관계
  - 구현(implements) 관계
  - import된 클래스 목록
- 추출된 클래스 관계 정보를 YAML 형태로 표준 출력(터미널)에 표시합니다.
- 동시에 `[디렉토리명]_classes.yaml` 형태의 파일로 결과를 저장합니다.

## 요구 사항

- Python 3.x
- `javalang` 라이브러리: `pip install javalang`
- `PyYAML` 라이브러리: `pip install pyyaml`

## 사용 방법

1. 본 스크립트를 `test.py`라는 파일로 저장합니다.
2. `python` 명령어를 사용하여 스크립트를 실행할 때, 대상 디렉토리명을 인자로 전달합니다.
   ```bash
   python test.py [DIRECTORY_NAME]
   ```
````

여기서 `[DIRECTORY_NAME]`은 `framework` 디렉토리 하위의 대상 모듈 디렉토리명입니다.

예를 들어, `ustra-mvc` 디렉토리를 조사하려면:

```bash
python test.py ustra-mvc
```

3. 스크립트가 실행되면 다음의 작업을 수행합니다:
   - `/Users/dvmoomoodv/Project/company/gsitm/framework/ustra-framework2.2-java/framework/[DIRECTORY_NAME]` 디렉토리를 재귀적으로 탐색합니다.
   - 모든 `.java` 파일을 파싱하고, 클래스 관계를 추출합니다.
   - 추출된 정보를 YAML로 터미널에 출력합니다.
   - `[DIRECTORY_NAME]_classes.yaml` 파일을 현재 작업 디렉토리에 생성하여 동일한 정보를 저장합니다.

## 출력 예시

터미널 출력 예(일부):

```yaml
com.example.MyClass:
  extends: com.example.ParentClass
  implements:
    - com.example.SomeInterface
  imports:
    - com.example.Dependency
    - com.other.Helper
com.example.ParentClass:
  extends: null
  implements: []
  imports:
    - com.foo.Bar
```

생성된 `ustra-mvc_classes.yaml` 파일에도 동일한 정보가 저장됩니다.

## 기타

- 로그 레벨은 기본적으로 `INFO`이며, 더 자세한 디버그 정보가 필요하면 `logging.basicConfig(level=logging.DEBUG)`로 변경할 수 있습니다.
- 문법 에러가 있는 자바 파일은 경고 로그와 함께 건너뛰며, 클래스 정보에 포함되지 않습니다.
- 필요에 따라 `print_as_yaml` 호출을 제거하거나, `save_as_yaml`만 남겨서 출력 형식을 조정할 수 있습니다.

```

```

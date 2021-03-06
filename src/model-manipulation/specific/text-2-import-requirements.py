import sys
import fileinput

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

def generateRequirements():
    with open(infile_name, mode="r", encoding="utf-8") as infile:
        with open(outfile_elements_name, mode="w", encoding='utf-8') as outfile_elements:
            outfile_elements.write('"ID";"Type";"Name";"Documentation"\n')
            with open(outfile_relations_name, mode="w", encoding='utf-8') as outfile_relations:
                outfile_relations.write('"ID";"Type";"Name";"Documentation";"Source";"Target"\n')
                counter = 0
                for line in infile:
                    if(line.startswith('P')):
                        # requirement
                        index = line.index('\t')
                        reqText = line[index+1:-1].replace(';', ',').replace('„','').replace('“','')
                        reqNum = line[1:index]
                        reqNum = reqNum.split(".")
                        outfile_elements.write('"ID-req-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}";"Requirement";"P{reqNum[0]:0>1}.{reqNum[1]:0>2}.{reqNum[2]:0>2}";"{reqText}"\n'.format(reqNum=reqNum, reqText=reqText, counter=counter))
                        outfile_elements.write('"ID-ass-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}";"Assessment";"P{reqNum[0]:0>1}.{reqNum[1]:0>2}.{reqNum[2]:0>2} -> ";""\n'.format(reqNum=reqNum, counter=counter))
                        outfile_relations.write('"";"AssociationRelationship";"";"";"ID-ass-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}";"ID-req-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}"\n'.format(reqNum=reqNum))
                        counter += 1
                    else:
                        # problem
                        print("!!!! PROBLEM ", line)
    print ("{} requirements DONE".format(counter))

def generateAssesments(chapter, count):
    with open(outfile_elements_name, mode="w", encoding='utf-8') as outfile_elements:
        outfile_elements.write('"ID";"Type";"Name";"Documentation"\n')
        with open(outfile_relations_name, mode="w", encoding='utf-8') as outfile_relations:
            outfile_relations.write('"ID";"Type";"Name";"Documentation";"Source";"Target"\n')
            for idAss in range(count):
                outfile_elements.write('"ID-ass-P5-{chapter:0>2}-{idAss:0>2}";"Assessment";"P5.{chapter:0>2}.{idAss:0>2} -> ";""\n'.format(chapter=chapter,idAss=idAss+1))
                outfile_relations.write('"";"AssociationRelationship";"";"";"ID-ass-P5-{chapter:0>2}-{idAss:0>2}";"ID-req-P5-{chapter:0>2}-{idAss:0>2}"\n'.format(chapter=chapter,idAss=idAss+1))
    print("assesment generation DONE")

def rewriteReqId():
    with open(infile_name, mode="r", encoding="utf-8") as infile:
        with open(outfile_elements_name, mode="w", encoding='utf-8') as outfile_elements:
            outfile_elements.write('"ID";"Type";"Name";"Documentation"\n')
            counter = 0
            for line in infile:
                parts = line.split(';')
                if((len(parts) > 1) and (parts[1] == '"Requirement"')):
                    counter += 1
                    parts[0] = '"ID-req-' + parts[2][1:9].replace('.','-')+ '"'
                    outfile_elements.write(';'.join(parts))
    print('{} requirements converted DONE'.format(counter))


    
# infile_name = 'C:/Projects_src/Work/temp/req.txt'
infile_name = 'C:/Projects_src/Work/MoJ/cpp/temp/cppelements.csv'
outfile_elements_name = 'C:/Projects_src/Work/temp/reqelements.csv'
outfile_relations_name = 'C:/Projects_src/Work/temp/reqrelations.csv'

generateAssesments(12,2)
# rewriteReqId()

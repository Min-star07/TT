# The process of data analysis

1. run test.sh @result_GEN, need to modify data file and pedestal file
2. run test.sh @result_ANA, need to mofdify ROB number , mode(1,2)
   2.1. Check every channel fit result according to PDF file
   2.2. Check fit parameters result according to PDF file, the problem channel would shown in the file ("check_channel.txt")
3. run test.sh @check@result_Check, need to file ("check_problem.txt") from step 2
4. run test.sh @ana@result_Check, need to modified problem channels according step 3
   4.1 You should check problem best result according result of checking, add the times number in the file ("check-channel.txt")
   4.2 Modify parameters (sigma1, Q1, and so on), run test.sh@step3
